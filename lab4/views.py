from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image

# Create your views here.
def index(request):
    image_data = open('lab4/image/charizad.jpg','rb').read()
    return HttpResponse(image_data, content_type='image/jpeg')
def thumbnail(request):
    response = Image.open('lab4/image/charizad.jpg')
    response = response.thumbnail((300,300))
    response = response.save("thumbnail_%s_%s" % ('lab4/image/charizad.jpg', "_".join(size)))
    return HttpResponse(response)
