from django.shortcuts import render
from django.http import HttpResponse
from thumbnails import get_thumbnail
# Create your views here.
def index(request):
    image_data = open('lab4/charizad.jpg','rb').read()
    return HttpResponse(image_data, content_type='image/jpeg')
def thumbnail(request):
    return HttpResponse(get_thumbnail('lab4/charizad.jpg', '300x300', crop='center'),content_type='image/jpeg')
