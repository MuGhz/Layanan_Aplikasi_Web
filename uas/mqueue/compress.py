import pika, json, zipstream, time, os, requests

RESOURCE_URL = 'http://172.22.0.2/oauth/resource'
credentials = pika.PlainCredentials('1406559055', '1406559055')
params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='ZIP_QUEUE', exchange_type='direct', durable=True)
result = channel.queue_declare()
queue_name = result.method.queue
channel.queue_bind(exchange='ZIP_QUEUE',queue=queue_name,routing_key='')
print ('[X] Waiting for logs')

def authorize(bearer):
    print("BEARER = ",bearer)
    headers = {}
    headers['Authorization'] = bearer
    response = requests.get(RESOURCE_URL,headers=headers)
    print(response)
    return response

def zip_file(ch, method, properties, body):
    time.sleep(5)
    try :
        msg = json.loads(body.decode("utf-8"))
        fname = msg['filename']
        location = 'uas/templates/uas/cache/'+fname
        size = msg['size']
        token = msg['token']
        print('filename : ', fname, 'location : ', location, ' size: ', size)
    except Exception as e:
        print ("[E] Error :",e)
    try :
        response = authorize(token)
        response = json.loads(response.text)
        print(response)
        sum = 0
        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        z.write(location)
        with open(location+'.zip','wb') as f:
            for data in z:
                f.write(data)
                sum += (len(data)/size)*100
                print("[X] compressing ",sum,"%")
                time.sleep(0.01)
                channel.basic_publish(exchange='ZIP_QUEUE',routing_key=fname,body=str(sum))
            print("[X] compress done")
    except Exception as e:
        print(e)

channel.basic_consume(zip_file, queue=queue_name, no_ack=True)

channel.exchange_declare(exchange='TRANS_FILE', exchange_type='fanout')
result = channel.queue_declare()
queue_name = result.method.queue
channel.queue_bind(exchange='TRANS_FILE',queue=queue_name,routing_key='')

def write_file(ch, method, properties, body):
    try:
        msg = json.loads(body.decode("utf-8"))
        file64 = msg['file']
        filename = msg['filename']
        print("write file :",filename)
        with open("uas/templates/uas/cache/"+filename, "wb") as fh:
            fh.write(base64.decodebytes(file64))
    except Exception as e:
        print(e)

channel.basic_consume(write_file, queue=queue_name, no_ack=True)


channel.start_consuming()
