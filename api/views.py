
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ipl.models import Schedule, PointsTable
from django.core import serializers

import pandas as pd

import json
import pickle
import numpy as np
from sqlalchemy import create_engine
import os

DB_USER=os.environ['DB_USER'].strip()
DB_PASSWORD=os.environ['DB_PASSWORD'].strip()

engine = create_engine('mysql+pymysql://'+DB_USER+':'+DB_PASSWORD+'@localhost/cricket_prediction', echo=False)

cols = ['runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5', 'striker',
       'non-striker', 'bat_team_Chennai Super Kings',
       'bat_team_Delhi Daredevils', 'bat_team_Kings XI Punjab',
       'bat_team_Kolkata Knight Riders', 'bat_team_Mumbai Indians',
       'bat_team_Rajasthan Royals', 'bat_team_Royal Challengers Bangalore',
       'bat_team_Sunrisers Hyderabad', 'bowl_team_Chennai Super Kings',
       'bowl_team_Delhi Daredevils', 'bowl_team_Kings XI Punjab',
       'bowl_team_Kolkata Knight Riders', 'bowl_team_Mumbai Indians',
       'bowl_team_Rajasthan Royals', 'bowl_team_Royal Challengers Bangalore',
       'bowl_team_Sunrisers Hyderabad']

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
       'Rising Pune Supergiants', 'Royal Challengers Bangalore',
       'Kolkata Knight Riders', 'Delhi Daredevils', 'Kings XI Punjab',
       'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
       'Kochi Tuskers Kerala', 'Pune Warriors', 'Delhi Capitals']

def predict_score_raw(runs, wickets, overs, runs_last_5, wickets_last_5, striker, non_striker, bat_team, bowl_team):
    bat_team='bat_team_'+bat_team
    bat_team_index=cols.index(bat_team)
    
    bowl_team='bowl_team_'+bowl_team
    bowl_team_index=cols.index(bowl_team)
    
    X_temp=np.array([int(runs), int(wickets), float(overs), int(runs_last_5), int(wickets_last_5), int(striker), int(non_striker)])
    X_pred=np.zeros(23)
    X_pred[0:7]=X_temp
    X_pred[bowl_team_index]=1
    X_pred[bat_team_index]=1
    
    model = pickle.load(open('model.pkl', 'rb'))
    predicted_score=round(model.predict([X_pred])[0])
    predict_final=f'{int(predicted_score-10)}-{int(predicted_score+10)}'
    return predict_final


def predict_winner_raw():
    fixtures = pd.read_sql('ipl_schedule',engine)
    fixtures.drop(['city','time'],axis=1,inplace=True)
    fixtures.drop(['id','day'],axis=1,inplace=True)
    fixtures=fixtures.iloc[0:56]
    pred_set = []

    teams_local=fixtures['team1'].unique()
    teams_local=sorted(teams_local)
    
    print(fixtures.shape)
    
    for index, row in fixtures.iterrows():
        X=np.zeros(16)
        X[teams_local.index(row['team1'])]=1
        X[teams_local.index(row['team2'])+8]=1
    
        model = pickle.load(open('matches_knn.pkl', 'rb'))
        pred_set.append(model.predict([X])[0])
    
    return pred_set
    

def predict_winner(request):
    table = predict_winner_raw()
    return JsonResponse({'status':'success','data':json.dumps(table)})


@csrf_exempt
@require_http_methods(["POST"])
def predict_score(request):
    keys = ['runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5', 'striker', 'non-striker', 'bat_team', 'bowl_team']

    if all(key in request.POST for key in keys):
        values = [request.POST[key] for key in keys]
        predicted_score=predict_score_raw(*values)
        return JsonResponse({'status': 'success', 'data':{'predicted_score': predicted_score}})
    else:
        return JsonResponse({'status': 'failed'})

def execute_query(sql):
    with engine.connect() as connection:
        result = connection.execute(sql)
        data = result.fetchall()
    return data


def get_match_winners(request):
    sql = "SELECT winner, COUNT(*) AS 'num' FROM matches GROUP BY winner ORDER BY COUNT(*) DESC"
    data=execute_query(sql)
    data_dict = {j[0]:j[1] for j in data}
    return JsonResponse({'status':'success','data':data_dict})


def get_season_match_winners(request, season):
    if 2008<=season<=2019:
        sql = f"SELECT winner, COUNT(*) AS 'num' FROM matches WHERE season='{season}' GROUP BY winner ORDER BY COUNT(*) DESC"
        data=execute_query(sql)
        data_dict = {j[0]:j[1] for j in data}
        return JsonResponse({'status':'success','data':data_dict})
    else:
        return JsonResponse({'status':'failed'})


def get_matches_played(request):
    matches={}
    for team in teams:
        sql=f"SELECT COUNT(*) FROM matches WHERE team1='{team}' OR team2='{team}'"
        with engine.connect() as connection:
            result = connection.execute(sql)
            matches[team]=result.fetchone()[0]
    
    return JsonResponse({'status':'success','data':matches})


def get_season_matches_played(request, season):
    if 2008<=season<=2019:
        matches={}
        for team in teams:
            sql=f"SELECT COUNT(*) FROM matches WHERE (team1='{team}' OR team2='{team}') AND season='{season}'"
            with engine.connect() as connection:
                result = connection.execute(sql)
                matches[team]=result.fetchone()[0]
        
        return JsonResponse({'status':'success','data':matches})
    else:
        return JsonResponse({'status':'failed'})


def get_max_moms(request):
    sql = "SELECT player_of_match, COUNT(*) FROM matches GROUP BY player_of_match ORDER BY COUNT(*) DESC LIMIT 15"
    data=execute_query(sql)
    data_dict = {j[0]:j[1] for j in data}
    return JsonResponse({'status':'success','data':data_dict})

def get_season_max_moms(request, season):
    if 2008<=season<=2019:
        sql = f"SELECT player_of_match, COUNT(*) FROM matches WHERE season='{season}' GROUP BY player_of_match ORDER BY COUNT(*) DESC LIMIT 5"
        data=execute_query(sql)
        data_dict = {j[0]:j[1] for j in data}
        return JsonResponse({'status':'success','data':data_dict})
    else:
        return JsonResponse({'status':'failed'})


def get_toss_details(request):
    sql = "SELECT COUNT(*) FROM matches WHERE toss_winner=winner"
    data1=execute_query(sql)[0][0]

    sql = "SELECT COUNT(*) FROM matches WHERE toss_winner!=winner"
    data2=execute_query(sql)[0][0]

    data_dict = {'toss_win-match_win': data1, 'toss_win-match_loss': data2}
    return JsonResponse({'status':'success','data':data_dict})

def get_season_toss_details(request, season):
    if 2008<=season<=2019:
        sql = f"SELECT COUNT(*) FROM matches WHERE toss_winner=winner AND season='{season}'"
        data1=execute_query(sql)[0][0]

        sql = f"SELECT COUNT(*) FROM matches WHERE toss_winner!=winner AND season='{season}'"
        data2=execute_query(sql)[0][0]
        
        data_dict = {'toss_win-match_win': data1, 'toss_win-match_loss': data2}
        return JsonResponse({'status':'success','data':data_dict})
    else:
        return JsonResponse({'status':'failed'})


def schedule(request):
    schedule_all = Schedule.objects.all()
    response=[]
    for match in schedule_all:
        response.append([match.team1, match.team2, match.time, match.date, match.city])

    return JsonResponse({'status': 'success', 'data': response})


def wickets(request):
    sql = "SELECT bowler, COUNT(*) FROM deliveries WHERE is_wicket=1 AND dismissal_kind!='run out' GROUP BY bowler ORDER BY `COUNT(*)` DESC LIMIT 15"
    data=execute_query(sql)
    data_dict = {j[0]:j[1] for j in data}
    return JsonResponse({'status':'success','data':data_dict})


def catches(request):
    sql="SELECT fielder, COUNT(*) FROM deliveries WHERE is_wicket=1 AND (dismissal_kind='caught' OR dismissal_kind='caught and bowled') GROUP BY fielder ORDER BY `COUNT(*)` DESC LIMIT 15"
    data=execute_query(sql)
    data_dict = {j[0]:j[1] for j in data}
    return JsonResponse({'status':'success','data':data_dict})

def batsman(request):

    sql="SELECT batsman, SUM(batsman_runs) as sum FROM deliveries GROUP BY batsman ORDER BY sum DESC LIMIT 15"
    data = execute_query(sql)
    data_dict = {j[0]:int(j[1]) for j in data}
    return JsonResponse({'status':'success','data':data_dict})



def predict_match_winner(team1, team2):
    teams_list = sorted([
        'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
        'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 
        'Delhi Capitals'
    ])
    
    X=np.zeros(16)
    X[teams_list.index(team1)] = 1
    X[teams_list.index(team2)+8] = 1
    
    model = pickle.load(open('matches_knn.pkl', 'rb'))
    winner = model.predict([X])

    if winner==team1:
        return {'winner': team1, 'loser': team2}
    else: 
        return {'winner': team2, 'loser': team1}

def qualifiers(response):
    points = PointsTable.objects.order_by('-points')[:4]

    qualifier1_set = {'team1':points[0].team,'team2':points[1].team}
    eliminator_set = {'team1':points[2].team,'team2':points[3].team}

    q1_winner=predict_match_winner(qualifier1_set['team1'], qualifier1_set['team2'])
    el_winner=predict_match_winner(eliminator_set['team1'], eliminator_set['team2'])
    q2_winner=predict_match_winner(el_winner['winner'], q1_winner['loser'])
    final_winner=predict_match_winner(q1_winner['winner'], q2_winner['winner'])

    data={'Qualifier 1': q1_winner, 'Eliminator': el_winner, 'Qualifier 2': q2_winner, 'Final': final_winner}

    return JsonResponse({'status': 'success', 'data': data})
