import pika, json,
credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = ''
channel.exchange_declare(exchange='ZIP_QUEUE', exchange_type='direct', durable=True)
result = channel.queue_declare()
queue_name = result.method.queue
channel.queue_bind(exchange='ZIP_QUEUE',queue=queue_name,routing_key='')
print ('[X] Waiting for logs')
channel.basic_consume(zip_file, queue=queue_name, no_ack=True)
channel.start_consuming()

def zip_file(ch, method, properties, body):
    try :
        msg = json.loads(body.decode("utf-8"))
        z = zipstream.ZipFile(mode='w', compression=ZIP_DEFLATED)
        z.write(msg["file"])
        for data in z:
            progress = len(data)/msg['size']
            print("[X] compressing ",progress,"%")
    except Exception as e:
        print ("[E] Error :",e)

def
