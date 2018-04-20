from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('math', views.math, name='math'),
    path('orchestrator', views.orchestrator, name='orchestrator'),
    path('check', views.check, name='check'),
    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
