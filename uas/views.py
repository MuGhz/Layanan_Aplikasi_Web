from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pika, json, requests

# Create your views here.
def index(request):
    return render(request,'uas/index.html')

def login(request):
    try :
        req = request.body.decode('utf-8')
        req = json.loads(req)
        myfile = request.FILES['userfile']
        blob = myfile.read()
        size = len(blob)
        send_message(req['username'],req['password'],myfile.name,size)
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
    url = 'http://host23014.proxy.infralabs.cs.ui.ac.id/uas/upload'
    files = {'userfile':myfile}
    req = requests.post(url, files=files)

def upload(request):
    folder = filename = os.path.dirname(__file__)+'/templates/uas/cache'
    myfile = request.FILES['userfile']
    fs = FileSystemStorage(location=folder)
    filename = fs.save(myfile.name, myfile)
    return JsonResponse({'status':'OK'},status=200)

def generate(request):
    pass
