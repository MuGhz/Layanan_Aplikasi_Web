import pika, json, zipstream, time
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
    time.sleep(5)
    try :
        msg = json.loads(body.decode("utf-8"))
        location = msg['file']
        size = msg['size']
        fname = msg['fname']
        sum = 0
        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        z.write(msg["file"])
        with open(location+'.zip','wb') as f:
            for data in z:
                f.write(data)
                sum += (len(data)/size)*100
                print("[X] compressing ",sum,"%")
                time.sleep(0.01)
                channel.basic_publish(exchange='ZIP_QUEUE',routing_key=fname,body=str(sum))
            print("[X] compress done")
    except Exception as e:
        print ("[E] Error :",e)

channel.basic_consume(zip_file, queue=queue_name, no_ack=True)
channel.start_consuming()
