from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from .models import User
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")
def login(request):
    if request.method == 'POST' :
        try :
            print(request.body)
            req = request.body.decode('utf-8')
            req = json.loads(req)
            r = utils.get_token(req['username'], req['password'])
        except Exception as e:
            print(e)
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        r = json.loads(r.text)
        response = {}
        response['status'] = 'ok'
        response['token'] = r['access_token']
        return JsonResponse(response,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
def users(request):
    if request.method == 'POST' :
        try :
            r = utils.authorize(request.META['HTTP_AUTHORIZATION'])
        except Exception as e:
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        r = json.loads(r.text)
        print(r)
        user_id = r['user_id']
        displayName = json.loads(request.body.decode('utf-8'))
        try :
            u = User.objects.get(username=user_id)
            response = {
                'status': 'error',
                'description': 'User telah memiliki displayName'
            }
            return JsonResponse(response,status=409)
        except ObjectDoesNotExist :
            u = User(username=user_id, displayName = displayName)
            u.save()
            userId = u.id
            response = {}
            response['status']= 'ok'
            response['userId'] = userId
            response['displayName'] = displayName
            return JsonResponse(response,status=200)
    elif request.method == 'GET' :
        return JsonResponse({},status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
#def comments(request,id=''):
