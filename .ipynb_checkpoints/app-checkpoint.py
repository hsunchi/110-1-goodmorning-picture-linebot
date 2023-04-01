#coding=utf-8
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply,ImageMessage,ImageSendMessage,QuickReplyButton,MessageAction
import string
import configparser
import random
from PIL import ImageFont, ImageDraw, Image

from random import choice

import library_init
import change_words
# import imgur_upload
import download_picture
import ngrok_upload
import mix_TextAndPic
import pandas as pd
app = Flask(__name__)

#LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))



#接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#學你說話
@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.type == 'text':
            #event.message.text[0]
            if event.message.text[0] == '$':
                                #僅隨機一句
                result = change_words.change_word(2,event.message.text[1:]) #得到一句語錄
                change_words.pic_picture(event.source.user_id) # Prepare Image 
                path = 'source_images/'+event.source.user_id+'.jpg'
                print(path)
                mix_TextAndPic.mix(result,path,event.source.user_id)#合成字跟圖片
                
                picture_link = ngrok_upload.upload(event.source.user_id)#圖片上傳至ngrok
                print(picture_link)
                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(original_content_url=picture_link,preview_image_url=picture_link)
                )
                

            elif event.message.text == "@隨機長輩圖":
                message=TextSendMessage(
                    text="請選擇想要的種類",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="早安",text="$morning")
                                ),
                            QuickReplyButton(
                                action=MessageAction(label="午安",text="$afternoon")
                                ),
                            QuickReplyButton(
                                action=MessageAction(label="晚安",text="$night")
                                ),
                            QuickReplyButton(
                                action=MessageAction(label="新年",text="$holiday#新年")
                                ),
                            QuickReplyButton(
                                action=MessageAction(label="聖誕",text="$christmas")
                                ),
                            QuickReplyButton(
                                action=MessageAction(label="週末",text="$holiday#週末")
                                )
                            ]
                        )
                    )
                line_bot_api.reply_message(
                    event.reply_token,
                    message
                )
                

            elif event.message.text == "@輸入文字":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = "please input your sentence\n請輸入文字")
                )
            elif event.message.text == "@輸入圖片":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = "please input your picture\n請上傳圖片")
                )
            else:#輸入文字
                result = event.message.text
                change_words.pic_picture(event.source.user_id) # Prepare Image 
                path = 'source_images/'+event.source.user_id+'.jpg'
                print("result.isdecimal():"+str(result.isdecimal()))
                
                if not is_contains_chinese(result): #處理英文分行（以三個字母為單位分行）
                    new_result = ""
                    splict_result = result.split()
                    print("splict_result:")
                    print(splict_result)
                    for i in range(len(splict_result)) :
                        if i%3 == 2:
                            new_result += (splict_result[i]+'，')
                        else:
                            new_result += (splict_result[i]+' ')
                    result = new_result
                print(result)
                
                mix_TextAndPic.mix(result,path,event.source.user_id)#合成字跟圖片

                picture_link = ngrok_upload.upload(event.source.user_id)#圖片上傳至ngrok
                print(picture_link)
                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(original_content_url=picture_link,preview_image_url=picture_link)
                )

        elif event.message.type == 'image': #輸入照片
                

            image_content = line_bot_api.get_message_content(event.message.id)
            download_picture.download_picture(image_content,event.source.user_id) #把傳給linebot的圖傳到我的本機
            result = change_words.change_word(1,"non") #得到一句語錄
            path = 'upload_image/'+event.source.user_id+'.jpg'
            
            mix_TextAndPic.mix(result,path,event.source.user_id)#合成字跟圖片

            picture_link = ngrok_upload.upload(event.source.user_id)#圖片上傳至ngrok
            print(picture_link)
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(original_content_url=picture_link,preview_image_url=picture_link)
            )
            
#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

if __name__ == "__main__":
    app.run()
