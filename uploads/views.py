from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Welcome to Muhammad Ghozi's webservices.")

def test(request):
    if request.method == 'POST' :
        folder = filename = os.path.dirname(__file__)+'/templates/uploads/cache'
        try :
            myfile = request.FILES['file']
            fs = FileSystemStorage(location=folder)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = folder + '/' + fs.url(filename)
            return render(request, 'uploads/uploads.html', {'uploaded_file_url': uploaded_file_url})
        except Exception as e:
            print(e)
    return render(request,'uploads/uploads.html')
def upload(request):
    return render(request, 'uploads/upload.js')
