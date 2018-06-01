import pika, json, zipstream
credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='ZIP_QUEUE', exchange_type='direct', durable=True)
result = channel.queue_declare()
queue_name = result.method.queue
channel.queue_bind(exchange='ZIP_QUEUE',queue=queue_name,routing_key='')
print ('[X] Waiting for logs')
def zip_file(ch, method, properties, body):
    try :
        msg = json.loads(body.decode("utf-8"))
        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        z.write(msg["file"])
        sum = 0
        with open(msg["file"]+'.zip', 'wb') as f:
            for data in z:
                sum += (len(data)/msg['size'])*100
                f.write(data)
                print("[X] compressing ",sum,"%")
            print("[X] compress done")
    except Exception as e:
        print ("[E] Error :",e)

channel.basic_consume(zip_file, queue=queue_name, no_ack=True)
channel.start_consuming()
