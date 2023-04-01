from PIL import ImageFont, ImageDraw, Image
def download_picture(image_content,user_id) :
    image_name = user_id+'.jpg'
    path='./upload_image/'+image_name
    with open(path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    img = Image.open(path)
    (w, h) = img.size
    if w <= 512:
        img = img.resize((w*2,h*2))
    else :
        img = img.resize((int(w*0.5),int(h*0.5)))
    img.save(path)