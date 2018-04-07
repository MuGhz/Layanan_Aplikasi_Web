from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def test(request):
    return render(request,'uploads/uploads.html')
def upload(request):
    return render(request, 'uploads/upload.php')
