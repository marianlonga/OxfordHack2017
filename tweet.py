from TwitterAPI import TwitterAPI

def tweet(text, image_name):
    CONSUMER_KEY = 'Xzv1c80TcwiqGAnFjZTIcXS14'
    CONSUMER_SECRET = 'TAD2fsfCXjfKIUO1Q94qlBvPyjT9XeZx8pFS4qcCsQHpD5DbhL'
    ACCESS_TOKEN_KEY = '903192995679391745-3eDwWYIVf6BMTaWjQhJ77Bg30faJBF9'
    ACCESS_TOKEN_SECRET = 'rre84yzmXHXLuF2juCZ14CpbFXudpESmrGlEwpI6UIHu8'

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    file = open(image_name, 'rb')
    data = file.read()
    r = api.request('statuses/update_with_media', {'status': text}, {'media[]': data})
    #print(r.status_code)