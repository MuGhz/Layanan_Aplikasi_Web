from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
