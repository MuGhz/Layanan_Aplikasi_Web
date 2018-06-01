from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os,pika, json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def upload(request):
    if request.method == 'POST' :
        folder = filename = os.path.dirname(__file__)+'/templates/lat_uas/cache'
        myfile = request.FILES['userfile']
        fs = FileSystemStorage(location=folder)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = folder + '/' + fs.url(filename)
        size = int(os.stat(uploaded_file_url).st_size)
        zipfile(uploaded_file_url,size)
        exc_method = '/exchange/ZIP_QUEUE/'+uploaded_file_url
        return render(request, 'lat_uas/zip.html', {'exc_method':exc_method})
    return render(request,'lat_uas/index.html')

def zipfile(filename,size):
    credentials = pika.PlainCredentials('1406559055', '1406559055')
    params= pika.ConnectionParameters('152.118.148.103',5672,'/1406559055',credentials)
    connection = pika.BlockingConnection(params)
    channel = ''
    channel = connection.channel()
    channel.exchange_declare(exchange='ZIP_QUEUE',exchange_type='direct',durable=True)
    msg = {}
    msg['file'] = filename
    msg['size'] = size
    msg = json.dumps(msg)
    channel.basic_publish(exchange='ZIP_QUEUE',routing_key='',body=msg)
    print ("[x] ZIP start")
    connection.close()
