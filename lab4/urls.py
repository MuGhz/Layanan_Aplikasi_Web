from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/thumbnail/$', views.thumbnail, name='thumbnail'),
    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
