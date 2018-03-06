from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import utils
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")
def login(request):
    if request.method == 'POST' :
        try :
            r = utils.get_token(request.POST['username'], request.POST['password'])
        except Exception as e:
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
#def users(request):

#def comments(request,id=''):
