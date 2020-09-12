from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction', views.prediction, name='prediction'),
    path('info',views.info,name='info'),
    path('visualization', views.visualization, name='visualization'),
    path('call_func',views.call_func,name='call_func'),
    # path('result', views.result, name='result'),
    path('schedule',views.schedule,name='schedule'),
    path('about', views.about, name='about'),
    path('match',views.match,name='match'),
    path('points',views.points_table,name='points'),
    path('qualifiers',views.qualifiers,name='qualifiers'),
    path('stats',views.stats,name='stats')
]
