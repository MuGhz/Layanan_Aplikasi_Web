from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('upload-progress.js', views.javascript, name='javascript'),
    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
