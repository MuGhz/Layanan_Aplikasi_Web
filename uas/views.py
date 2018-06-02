from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pika, json, requests, os, base64

# Create your views here.
def index(request):
    return render(request,'uas/index.html')

def login(request):
    try :
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        print('username : ',username," password :",password)
        myfile = request.FILES['userfile']
        myfile.seek(0, os.SEEK_END)
        size = myfile.tell()
        send_message(username,password,myfile.name,size)
        send_file(myfile)
        exc_method = '/exchange/ZIP_QUEUE/'+myfile.name
        return render(request,'uas/result.html',{'exc_method':exc_method})
    except Exception as e:
        print(e)
    return render(request,'uas/result.html')

def send_message(username,password,fname,size):
    credentials = pika.PlainCredentials('1406559055', '1406559055')
    params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='ORC_CREDENTIALS',exchange_type='fanout')
    msg ={}
    msg['username'] = username
    msg['password'] = password
    msg['filename'] = fname
    msg['size'] = size
    msg = json.dumps(msg)
    channel.basic_publish(exchange='ORC_CREDENTIALS',routing_key='',body=msg)
    print("[x] send credentials to orchestrator")
    connection.close()

def send_file(myfile):
    credentials = pika.PlainCredentials('1406559055', '1406559055')
    params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='TRANS_FILE',exchange_type='fanout')
    file64 = base64.b64encode(myfile.read())
    file64 = file64.decode("utf-8")
    msg = {}
    msg['file'] = file64
    msg['filename'] = myfile.name
    msg = json.dumps(msg)
    channel.basic_publish(exchange='TRANS_FILE',routing_key='',body=msg)
    print("[x] file telah dikirim.")
    connection.close()

def upload(request):
    folder = filename = os.path.dirname(__file__)+'/templates/uas/cache'
    myfile = request.FILES['userfile']
    fs = FileSystemStorage(location=folder)
    filename = fs.save(myfile.name, myfile)
    return JsonResponse({'status':'OK'},status=200)

def generate(request):
    pass
