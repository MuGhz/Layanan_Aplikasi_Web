from django.shortcuts import render
from thumbnails import get_thumbnail

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Lab4 - Muhammad Ghozi")
def thumbnail(request):
    return HttpResponse(get_thumbnail('charizad.jpg', '300x300', crop='center'))
