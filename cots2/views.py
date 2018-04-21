from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests, json, zeep

def call_request(var1,var2,operation):
    wsdl = 'http://host20099.proxy.infralabs.cs.ui.ac.id/matematika.xml'
    client = zeep.Client(wsdl=wsdl)
    if operation == 'tambah':
        payloads = {'a':var1,'b':var2}
        response = requests.get('http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php',params=payloads,timeout=120)
        if response.status_code != requests.codes.ok :
            return call_request(var1,var2,operation)
        r = json.loads(response.text)
        return r['hasil']
    elif operation == 'kurang':
        payloads = {'a':var1,'b':var2}
        response = requests.post('http://host20099.proxy.infralabs.cs.ui.ac.id/kurang.php',data=payloads,timeout=120)
        if response.status_code != requests.codes.ok :
            return call_request(var1,var2,operation)
        return response.text
    elif operation == 'kali':
        var1 = str(var1)
        var2 = str(var2)
        header = {'Argumen-A':var1,'Argumen-B':var2}
        response = requests.get('http://host20099.proxy.infralabs.cs.ui.ac.id/kali.php',headers=header,timeout=120)
        if response.status_code != requests.codes.ok :
            return call_request(var1,var2,operation)
        return response.text
    elif operation == 'bagi':
        var1 = str(var1)
        var2 = str(var2)
        header = {'Argumen-A':var1,'Argumen-B':var2}
        response = requests.head('http://host20099.proxy.infralabs.cs.ui.ac.id/bagi.php',headers=header,timeout=120)
        if response.status_code != requests.codes.ok :
            return call_request(var1,var2,operation)
        return response.headers['hasil']
    elif operation == 'mod':
        return client.service.modulo(var1,var2)
    elif operation == 'round':
        return client.service.round_number(var1)
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def math(request):
    return render(request,'cots2/math.html')

def orchestrator(request):
    if request.method == 'GET':
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        payloads={'a':a,'b':b,'c':c,'d':d}
        req1 = requests.get('http://host22014.proxy.infralabs.cs.ui.ac.id/cots2/r1',params=payloads,timeout=1000)
        req2 = requests.get('http://host23014.proxy.infralabs.cs.ui.ac.id/cots2/r2',params=payloads,timeout=1000)
        req3 = requests.get('http://host24014.proxy.infralabs.cs.ui.ac.id/cots2/r3',params=payloads,timeout=1000)
        req1 = json.loads(req1.text)
        req2 = json.loads(req2.text)
        req3 = json.loads(req3.text)
        sum = req1['hasil'] + req2['hasil'] - req3['hasil']
        res = {'hasil':sum}
        return render(request,'cots2/math.html',{'hasil':hasil})
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)

def r1(request):
    if request.method == 'GET':
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        var1 = call_request(a,b,'tambah')
        var2 = call_request(var1,c,'bagi')
        var3 = call_request(var2,0,'round')
        var4 = call_request(var3,d,'mod')
        res = {'hasil':var4}
        return JsonResponse(res,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)

def r2(request):
    if request.method == 'GET':
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        var1 = call_request(a,d,'tambah')
        var2 = call_request(b,c,'mod')
        var3 = call_request(var1,var2,'bagi')
        var4 = call_request(var3,0,'round')
        res = {'hasil':var4}
        return JsonResponse(res,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)

def r3(request):
    if request.method == 'GET':
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        var1 = call_request(a,c,'kurang')
        var2 = call_request(b,c,'bagi')
        var3 = call_request(var1,var2,'kali')
        var4 = call_request(var3,0,'round')
        res = {'hasil':var4}
        return JsonResponse(res,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
