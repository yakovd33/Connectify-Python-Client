import requests

def post (url, post_data) :
    r = requests.post(url, data = post_data)

    if r.status_code == 500 or r.status_code == 200 :
        return r.text
    else :
        return False

def get (url) :
    r = requests.get(url)

    if r.status_code == 500 or r.status_code == 200 :
        return r.text
    else :
        return False