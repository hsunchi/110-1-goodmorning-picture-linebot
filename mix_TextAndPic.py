from PIL import ImageFont, ImageDraw, Image
from random import choice
import numpy as np
def mix(result,path,user_id):
    result_list = []
    result_list = stringToList(result)
    string_size = len(result_list)
    num = 0
    for i, word in enumerate(result_list):
        result_list.insert(num+1, '\n')
        num += 2
        if i == string_size-1:
            break
    output_string = ''.join(result_list)



    img = Image.open(path)
    R, G, B = np.asarray(img).mean(axis=0).mean(axis=0).astype(int)

    position = (25, 35)
    font_list = ['NotoSansTC-Black.otf', 'NotoSansTC-Medium.otf',
                 'NotoSerifTC-Black.otf', 'NotoSerifTC-Bold.otf']
    lower = 'NotoSerifTC-Black.otf'
    upper = 'NotoSerifTC-Bold.otf'
    fill_lower = (0, 0, 0, 0)
    fill_upper = (255-R, 255-G, 0, 0)
    text = output_string
    text_length = len(text)
    font_size = 48
    if text_length >= 17:
        font_size = 40
        position = (20, 30)

    backup_img = img.copy()
    draw = ImageDraw.Draw(img)
    # Set font style & font size
    font_tmp = choice(font_list)
    font_lower = ImageFont.truetype('Open_Data/Fonts/%s' % lower, font_size)
    font_upper = ImageFont.truetype('Open_Data/Fonts/%s' % upper, font_size)
    
    draw.text( position, text, font=font_lower, fill=fill_lower ,stroke_width=1)
    draw.text( position, text, font=font_upper, fill=fill_upper ,stroke_width=0)
    # display(img)
    img.save('generated_images/'+user_id+'.jpg')
    img = backup_img.copy()
    
def stringToList(string):
    listRes = string.split("，")
    return listRes