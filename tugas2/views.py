from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests, json

def call_request(var1,var2,operation):
    if operation == 'tambah':
        payloads = {'a':var1,'b':var2}
        response = requests.get('http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php',params=payload,timeout=120)
        if response.status_code != requests.codes.ok :
            return call_request(var1,var2,operation)
        r = json.loads(response.text)
        return r['hasil']
    elif operation == 'kurang':
        payloads = {'a':var1,'b':var2}
        response = requests.post('http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php',data=payload,timeout=120)
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
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def math(request):
    return render(request,'tugas2/math.html')

def orchestrator(request):
    if request.method == GET:
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        var1 = call_request(a,b,'tambah')
        var2 = call_request(c,b,'kali')
        var3 = call_request(var1,c,'tambah')
        var1 = call_request(var1,c,'kali')
        var2 = call_request(var2,d,'kali')
        var3 = call_request(var3,d,'kali')
        var1 = call_request(var1,d,'bagi')
        var2 = call_request(var2,a,'bagi')
        var3 = call_request(var3,c,'bagi')
        sum = call_request(var1,var3,'tambah')
        sub = call_request(sum,var2,'kurang')
        res = {'hasil':sub}
        return JsonResponse(res,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)

def check(request):
    if request.method == GET:
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')
        d = request.GET.get('d')
        sum = (((a+b)*c)/d) + (((a+b+c)*d)/c) - (((c*b)*d)/a)
        response = {
            'hasil': sum
        }
        return JsonResponse(response,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
