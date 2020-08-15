from django.urls import path
from . import views

urlpatterns = [
    path('predict_score', views.predict_score, name='home'),
    path('match_winners',views.get_match_winners,name='match_winners'),
    path('season_match_winners/<int:season>',views.get_season_match_winners,name='season_match_winners'),

    path('match_played',views.get_matches_played,name='match_played'),
    path('season_match_played/<int:season>',views.get_season_matches_played,name='season_match_played'),
    # path('maximum_winners',views.maximum_winners,name='maximum_winners')
]
 