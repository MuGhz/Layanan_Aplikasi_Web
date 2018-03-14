from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image

# Create your views here.
def index(request):
    image_data = open('lab4/charizad.jpg','rb').read()
    return HttpResponse(image_data, content_type='image/jpeg')
def thumbnail(request):
    image_data = open('lab4/charizad.jpg','rb').read()
    return HttpResponse(Image.open(image_data).thumbnail((300,300)).save("thumbnail_%s_%s" % (image_data, "_".join(((300,300))))))
