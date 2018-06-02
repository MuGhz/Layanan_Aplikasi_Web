import pika, json, datetime, time
credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='TIME',exchange_type='fanout')
while(True):
    timenow = str(datetime.datetime.now())
    print(timenow)
    channel.basic_publish(exchange='TIME',routing_key='',body=timenow)
    time.sleep(1)
connection.close()
