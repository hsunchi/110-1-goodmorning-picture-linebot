ngrok_url = "https://e9f6-140-113-110-105.ngrok.io"


def upload(user_id):
    PATH = "generated_images/"+user_id+".jpg"

    local_save = './static/'+user_id+'.png'
    with open(PATH, 'rb') as f:
        data = f.read()
    with open(local_save, 'wb') as fd:
        fd.write(data)
    return ngrok_url+'/static/'+user_id+'.png'
                
		