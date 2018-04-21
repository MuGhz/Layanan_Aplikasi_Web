from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('math', views.math, name='math'),
    path('orchestrator', views.orchestrator, name='orchestrator'),
    path('r1', views.r1, name='r1'),
    path('r2', views.r2, name='r2'),
    path('r3', views.r3, name='r3'),

    #re_path(r'v1/comments/(?:(?P<id>\d+))?$',views.comments, name="comments")
]
