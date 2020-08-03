from django.urls import path
from . import views

urlpatterns = [
    path('predict-score', views.predict_score, name='home'),
]
