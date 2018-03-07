from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Client
from django.core.exceptions import ObjectDoesNotExist
import json, string, random, hmac, hashlib, base64
# Create your views here.
def secret_generator(size=10,chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
def encode_text(plaintext,secret):
    return base64.b64encode(hmac.new(secret, msg=plaintext, digestmod=hashlib.sha256).digest())
def md5_text(text):
    m = hashlib.md5(text.encode('utf-8'))
    return m.hexdigest()
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's oauth webservice.")
def login(request):
    if request.method == 'POST':
        try :
            username = request.POST['username']
            password = request.POST['password']
            xsign = request.META['X-Service-Signature']
        except Exception :
            response = {
                'status': 'Error',
                'description': 'Bad Request'
            }
            return JsonResponse(response,status=400)
        try :
            c = Client.objects.get(username=username)
        except ObjectDoesNotExist:
             response = {
                 'status': 'Error',
                 'description': 'Username and password not found'
             }
             return JsonResponse(response,status=404)
        key = encode_text(request.POST,c.secret)
        if(key == xsign) :
            response = {}
            response['status'] = 'ok'
            rdm = secret_generator
            md5result =md5_text(rdm)
            response['token'] = md5result
            try :
                t = Token.objects.get(username=username)
                t.token = md5result
                t.save()
            except ObjectDoesNotExist:
                t = Token(username=username,token=md5result)
                t.save
            return JsonResponse(response,status=200)
        else :
            response = {
                'status': 'Error',
                'description': 'Unauthorize'
            }
            return JsonResponse(response,status=401)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
def register(request):
    if request.method == 'POST':
        try :
            username = request.POST['username']
            password = request.POST['password']
            displayName = request.POST['displayName']
        except Exception :
            response = {
                'status': 'Error',
                'description': 'Bad Request'
            }
            return JsonResponse(response,status=400)
        try :
            c = Client.objects.get(username=username)
            response = {
                'status': 'error',
                'description': 'User telah teregister'
            }
            return JsonResponse(response,status=409)
        except ObjectDoesNotExist :
            secret = secret_generator()
            c = Client(username=username,password=password,displayName=displayName,secret=secret)
            c.save()
            userId = c.id
            response={}
            response['status'] = 'ok'
            response['userId'] = userId
            response['displayName'] = displayName
            response['secret'] = secret
            return JsonResponse(response,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
