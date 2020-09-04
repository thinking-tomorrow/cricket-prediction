from django.urls import path
from . import views

urlpatterns = [
    path('predict_score', views.predict_score, name='home'),
    path('match_winners',views.get_match_winners,name='match_winners'),
    path('season_match_winners/<int:season>',views.get_season_match_winners,name='season_match_winners'),

    path('match_played',views.get_matches_played,name='match_played'),
    path('season_match_played/<int:season>',views.get_season_matches_played,name='season_match_played'),

    path('max_moms',views.get_max_moms,name='max_moms'),
    path('season_max_moms/<int:season>',views.get_season_max_moms,name='season_max_moms'),

    path('toss_details',views.get_toss_details,name='toss_details'),
    path('season_toss_details/<int:season>',views.get_season_toss_details,name='season_toss_details'),

    path('schedule', views.schedule, name='schedule'),
    path('winner',views.predict_winner,name='winner')
]
 