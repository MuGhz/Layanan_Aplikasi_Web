from django.shortcuts import render
from django.http import HttpResponse
from sorl.thumbnail import get_thumbnail
# Create your views here.
def index(request):
    image_data = open('lab4/charizad.jpg','rb').read()
    return HttpResponse(image_data, content_type='image/jpeg')
def thumbnail(request):
    im = get_thumbnail('lab4/charizad.jpg','300x300',crop='center',quality=99)
    return HttpResponse(im, content_type='image/jpeg')
