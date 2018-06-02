import pika,json
credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='ORC_CREDENTIALS', exchange_type='fanout')
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
    except Exception as e:
        print ("[E] Error :",e)

channel.basic_consume(orches, queue=queue_name, no_ack=True)
channel.start_consuming()
