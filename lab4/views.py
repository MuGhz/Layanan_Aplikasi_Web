from django.shortcuts import render
from thumbnails import get_thumbnail

# Create your views here.
def index(request):
    return HttpResponse(get_thumbnail('charizad.jpg', '300x300', crop='center'))
