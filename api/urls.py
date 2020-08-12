from django.urls import path
from . import views

urlpatterns = [
    path('predict-score', views.predict_score, name='home'),
    path('winners',views.matches,name='winners'),
    path('maximum_winners',views.maximum_winners,name='maximum_winners')
]
