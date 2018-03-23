from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PIL import Image
from datetime import datetime
import os
# Create your views here.
def index(request):
    image_data = open('lab4/image/charizad.jpg','rb').read()
    return HttpResponse(image_data, content_type='image/jpeg')
def thumbnail(request):
    filename = os.path.dirname(__file__)+'/image/charizad'
    thumbnail_file = filename+'-thumbnail.jpg'
    size = 300,300
    response = Image.open(filename+'.jpg')
    response.thumbnail(size)
    response.save(filename + '-thumbnail.jpg',"JPEG")
    return HttpResponse(open(thumbnail_file,'rb'), content_type='image/jpeg')
def add(request):
    if request.method == 'GET' :
        try :
            a = (int) request.GET.get('a')
        except :
            response = {
                'status': '400',
                'description': 'Bad Request. a is not integer'
            }
            return JsonResponse(response,status=400)
        try :
            b = (int) request.GET.get('b')
        except :
            response = {
                'status': '400',
                'description': 'Bad Request. b is not integer'
            }
            return JsonResponse(response,status=400)
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " :: A = " + a + " :: B = " + b
        logfile = os.path.dirname(__file__)+'/log/logfile.txt'
        log = open(logfile, 'a')
        log.write(data)
        log.close()
        if a > 0 and b > 0 :
            sum = a+b
            response = {
                'status': '200',
                'hasil': sum
            }
            return JsonResponse(response,status=200)
        else :
            response = {
                'status': '400',
                'description': 'Bad Request. number must be positive'
            }
            return JsonResponse(response,status=400)
    else :
        response = {
            'status': '400',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
