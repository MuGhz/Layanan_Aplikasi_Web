from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Lab4 - Muhammad Ghozi")
def thumbnail(request):
    return HttpResponse("this is thumbnail")
