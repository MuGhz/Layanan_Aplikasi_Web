from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload'),
    path('generate', views.generate, name='generate')

]
