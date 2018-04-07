from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def test(request):
    return render(request,'uploads/uploads.html')
def upload(request):
    folder = filename = os.path.dirname(__file__)+'/templates/uploads/cache'
    myfile = request.FILES['file']
    fs = FileSystemStorage(location=folder)
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    return render(request, 'uploads/uploads.html')
