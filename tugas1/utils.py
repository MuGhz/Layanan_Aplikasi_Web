import requests

CLIENT_ID = '2Byfk7psd7nEc836XHGZ3ctZLsehIHPQ'
CLIENT_SECRET = 'nM33J6jYIWrJw8W8qM9RVEyBxWqcDdbD'
GRANT_TYPE = 'password'
OAUTH_URL = 'http://172.22.0.2/oauth/token'
RESOURCE_URL = 'http://172.22.0.2/oauth/resource'

def get_token(username,password):
    payloads = {'username': username, 'password': password, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': GRANT_TYPE}
    response = requests.post(OAUTH_URL, data=payloads)
    return response

def authorize(bearer):
    headers['Authorization'] = bearer
    response = requests.get(RESOURCE_URL,headers=headers)
    return response
