from django.shortcuts import render
from django.http import HttpResponse
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
        a = request.GET.get('a')
        b = request.GET.get('b')
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " :: A = " + a + " :: B = " + b
        logfile = os.path.dirname(__file__)+'/log/logfile.txt'
        log = open(logfile, 'a')
        log.write(data)
        log.close()
        if isinstance(a,int) and isinstance(b,int) :
            sum = a+b
            response = {
                'status': '200',
                'hasil': sum
            }
            return JsonResponse(response,status=200)
        elif not isinstance(a,int) :
            response = {
                'status': '400',
                'description': 'Bad Request. a is not integer'
            }
            return JsonResponse(response,status=400)
        elif not isinstance(b,int) :
            response = {
                'status': '400',
                'description': 'Bad Request. b is not integer'
            }
            return JsonResponse(response,status=400)
    else :
        response = {
            'status': '400',
            'description': 'Bad Request'
        }
        return JsonResponse(response,status=400)
