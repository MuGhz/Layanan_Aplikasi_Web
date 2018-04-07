from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('upload.php', views.upload, name='upload'),
    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
