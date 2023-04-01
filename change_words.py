import random
import library_init
from ArticutAPI import Articut
from gensim.models import word2vec
import os
from matplotlib import pyplot as plt
from PIL import ImageFont, ImageDraw, Image
from ArticutAPI import Articut
from pprint import pprint
from random import choice
import pandas as pd

username = "tzerjen@gmail.com" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
apikey   = "LgbUF#o%Rm4eHmIUi@kgx!H&2p9$IY3" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
articut = Articut(username, apikey)

model = word2vec.Word2Vec.load('wearebest.model')
words = list(model.wv.index_to_key)

POS = library_init.load_POS()
DoNotChange = library_init.load_DoNotChange()
badword = library_init.load_badword()
dataset_txt = library_init.load_dataset()

#選取要的dataset
#dataset_type = 1 >>>>>>全部隨機
#dataset_type = 2 >>>>>>種類隨機
def choose_dataset(dataset_type,category_type):
    if dataset_type == 1:
        return dataset_txt
    elif dataset_type == 2:#種類隨機
        if category_type.find("#") != -1:
            category = category_type.split('#')
            category_type = category[0]
            holiday_name = category[1]
        df = pd.read_csv('dataset.csv')
        filter = (df['category'] == category_type)
        dataset_csv = df[filter]
        data_choose = dataset_csv['content'].tolist()
        if category_type == "holiday":
            new_data_choose = []
            for line in data_choose:
                line = line.replace("新年", holiday_name)
                line = line.replace("假日", holiday_name)
                line = line.replace("中秋節", holiday_name)
                new_data_choose.append(line)
            return new_data_choose
        else:
            return data_choose
    
#僅隨機一句
#dataset_type = 1 >>>>>>全部隨機
#dataset_type = 2 >>>>>>種類隨機
def change_word(dataset_type,category_type):
    result_list = []
    dataset = choose_dataset(dataset_type,category_type)
    line = random.choice(dataset)
    result_list.append(line)
    print("原始句子：",line)
    resultDICT = articut.parse(line)
    result = ""
    print("POS：",POS)
    for result_obj in resultDICT['result_obj'] :
        for i in result_obj :
            if(i['pos'] in POS):
                similar_word_list = []
                if i['text'] in words and i['text'] not in DoNotChange:
                    similar_word = model.wv.most_similar(i['text'])
                    print(f'target = {i["text"]}\nsimilar_word[:5]={similar_word[:5]}' )
                    for a_similar_word in similar_word[:5] :
                        if a_similar_word[1] > 0.655 and a_similar_word[0] not in badword:
                            similar_word_list.append(a_similar_word[0])
                    if similar_word_list != [] :
                        result +=random.choice(similar_word_list)
                    else :
                        result += i['text']
                else:
                    result += i['text']
            else :
                result += i['text']
    
    print("新句子：",result,"\n")
    result_list.append(result)
    result = choice(result_list)
    return result

def pic_picture(user_id):
    pic_path = 'lotus256_out/lotus256_out/'
    pic_file = os.listdir(pic_path)
    sample = random.sample(pic_file,1)
    img = Image.open(pic_path+sample[0])
    img = img.resize((512, 512))
    # (w, h) = img.size
    # if w <= 256:
    #     img = img.resize((w*2,h*2))
    # else :
    #     img = img.resize((w*0.5,h*0.5))
    img.save('source_images/'+user_id+'.jpg')
    
