from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
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
    response = response.thumbnail(size)
    response = response.save(filename+'-thumbnail.jpg',"JPEG")
    return HttpResponse(response)
