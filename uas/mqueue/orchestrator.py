import pika,json

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

credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='ORC_CREDENTIALS', exchange_type='fanout')
channel_compress = connection.channel()
channel_compress.exchange_declare(exchange="ZIP_QUEUE", exchange_type='direct', durable=True)
result = channel.queue_declare()
queue_name = result.method.queue
channel.queue_bind(exchange='ORC_CREDENTIALS',queue=queue_name,routing_key='')
print ('[X] Waiting for logs')

def orches(ch, method, properties, body):
    try :
        msg = json.loads(body.decode("utf-8"))
        username = msg['username']
        password = msg['password']
        fname = msg['filename']
        size = msg['size']
        token = get_token(username,password)
        channel_compress.basic_publish(exchange='ZIP_QUEUE',routing_key='',body={'filename':fname,'token':token,'size':size})
    except Exception as e:
        print ("[E] Error :",e)

channel.basic_consume(orches, queue=queue_name, no_ack=True)
channel.start_consuming()
