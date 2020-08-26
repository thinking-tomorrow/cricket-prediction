from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction', views.prediction, name='prediction'),
    path('info',views.info,name='info'),
    path('visualization', views.visualization, name='visualization'),
    path('call_func',views.call_func,name='call_func'),
    # path('result', views.result, name='result'),
    path('schedule',views.schedule,name='schedule')
]
