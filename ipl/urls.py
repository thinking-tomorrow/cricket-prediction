from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction', views.prediction, name='prediction'),
    path('info',views.info,name='info'),
    path('visualization', views.visualization, name='visualization')
    # path('result', views.result, name='result')
]
