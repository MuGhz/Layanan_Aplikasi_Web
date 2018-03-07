from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from .models import User, Comment
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
        displayName = json.loads(request.body.decode('utf-8'))['displayName']
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
        try :
            r = utils.authorize(request.META['HTTP_AUTHORIZATION'])
        except Exception as e:
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        if page == None or limit == None :
            response = {}
            response['status'] = 'error'
            response['description'] = 'parameter not completed'
            return JsonResponse(response,status=400)
        max_query = int(page) * int(limit)
        offset = max_query - int(limit)
        total = User.objects.all()
        all_user = total[offset:max_query]
        print(all_user)
        response ={
        'status':'ok',
        'page':page,
        'limit':limit,
        'total':total.count(),
        'data':list(all_user.values())
        }
        return JsonResponse(response,status=200)
    else :
        response = {
            'status': 'Error',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)

def comments(request,id=''):
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
        req = json.loads(request.body.decode('utf-8'))
        try:
            cmn = req['comment']
            c = Comment(comment=cmn,createdBy=user_id)
            c.save()
            data = {}
            data['id'] = c.id
            data['comment'] = cmn
            data['createdBy'] = user_id
            data['createdAt'] = c.createdAt
            data['updatedAt'] = c.updatedAt
            response={'status':'ok','data':data}
            return JsonResponse(response,status=200)
        except Exception as e:
            print(e)
            response = {
                'status': 'Error',
                'description': 'Bad Request'
            }
            return JsonResponse(response,status=400)
    elif request.method == 'GET' :
        if id == '' :
            return JsonResponse({'status':'WIP'},200)
        else :
            try :
                c = Comment.objects.get(id=id)
            except Exception as e:
                print(e)
                response = {
                    'status': 'Error',
                    'description': 'Bad Request'
                }
                return JsonResponse(response,status=400)
            data = {}
            data['id'] = id
            data['comment'] = c.comment
            data['createdBy'] = c.createdBy
            data['createdAt'] = c.createdAt
            data['updatedAt'] =  c.updatedAt
            response = {
            'status':'ok',
            'data':data
            }
            return JsonResponse(response,status=200)
        return JsonResponse({'status':'WIP'},200)
    elif request.method == 'PUT' :
        return JsonResponse({'status':'WIP'},200)
    elif request.method == 'DELETE' :
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

        try :
            id = json.loads(request.body.decode('utf-8'))['id']
        except Exception as e:
            print(e)
            response = {}
            response['status'] = 'error'
            response['description'] = 'parameter not completed'
            return JsonResponse(response,status=400)

        try :
            c = Comment.objects.get(id=id)
        except Exception as e:
            print(e)
            response = {
                'status': 'Error',
                'description': 'Bad Request'
            }
        if user_id != c.createdBy :
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        else :
            c.delete()
            response = {}
            response['status'] = 'ok'
            return JsonResponse(response,status=200)
