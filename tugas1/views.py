from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        user_list = User.objects.all()
        paginator = Paginator(user_list, limit)
        try :
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        response ={
        'status':'ok',
        'page':page,
        'limit':limit,
        'total':user_list.count(),
        'data':list(users.values())
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
        try :
            r = utils.authorize(request.META['HTTP_AUTHORIZATION'])
        except Exception as e:
            print(e)
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        r = json.loads(r.text)
        print(r)
        user_id = r['user_id']
        try :
            cmn = json.loads(request.body.decode('utf-8'))['comment']
        except Exception as e:
            print(e)
            response = {'status':'error', 'description' : 'parameter not completed'}
            return JsonResponse(response,status=400)
        if id == '' :
            response = {'status':'error', 'description' : 'parameter not completed'}
            return JsonResponse(response,status=400)
        else :
            try :
                c = Comment.objects.get(id=id)
            except Exception as e:
                print("error ketika mengambil comment berdasarkan id")
                response = {
                    'status': 'Error',
                    'description': 'Bad Request'
                }
                return JsonResponse(response,status=400)
        if user_id != c.createdBy :
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        else :
            c.comment = cmn
            c.save()
            data={}
            data['id'] = c.id
            data['comment'] = c.comment
            data['createdBy'] = c.createdBy
            data['createdAt'] = c.createdAt
            data['updatedAt'] = c.updatedAt
            response={'status':'ok','data':data}
            return JsonResponse(response,status=200)
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

        if id == '' :
            response = {'status':'error', 'description' : 'parameter not completed'}
            return JsonResponse(response,status=400)
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
        if user_id != c.createdBy :
            response = {
                'status': 'Error',
                'description': 'Unauthorized'
            }
            return JsonResponse(response,status=401)
        else :
            c.delete()
            return JsonResponse({'status':'ok'},status=200)
