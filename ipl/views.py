from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from .models import Schedule, PointsTable, OriginalPointsTable
from django.views.decorators.clickjacking import xframe_options_exempt
import datetime, time
import pytz
from sqlalchemy import create_engine
import os

DB_USER=os.environ['DB_USER'].strip()
DB_PASSWORD=os.environ['DB_PASSWORD'].strip()
ROOT=os.environ['ROOT_URL'].strip()

engine = create_engine('mysql+pymysql://'+DB_USER+':'+DB_PASSWORD+'@localhost/cricket_prediction', echo=False)

def execute_query(sql):
    with engine.connect() as connection:
        result = connection.execute(sql)
        data = result.fetchall()
    return data


def scrape_schedule():

    source = requests.get("https://www.icccricketschedule.com/vivo-ipl-2020-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/").text
    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')

    matches_rows = table.find_all('tr')
    matches_rows=matches_rows[1:]

    for matches in matches_rows:

        new = matches.find_all('td')
        new = list(map(lambda x:str(x.text).replace(',', ''), new))
        print(new[0])

        matches = Schedule()
        matches.team = new[1]
        matches.date = new[2]
        matches.day = new[3]
        matches.time = new[4]
        matches.city = new[6]

        matches.save()        

def home(request):
    today = datetime.date.today()
    today = today.strftime('%Y-%m-%d')

    next_game = Schedule.objects.filter(new_date=today)[0]
    team1 = next_game.team1
    team2 = next_game.team2
    date = next_game.new_date
    game_time = next_game.time

    year=date.year
    month=date.month
    day=date.day
    hour, minute=game_time.split(' ')[1].split(':')
    hour=int(hour)+12

    last_game = Schedule.objects.filter(new_date__lt=today)
    last_game  = last_game[len(last_game)-1]
    last_team1 = last_game.team1
    last_team2 = last_game.team2
    last_winner= last_game.original_winner

    date_time=datetime.datetime(year, month, day, hour, int(minute))
    return render(request, 'home.html',{'team1':team1,'team2':team2, 'date': str(date_time), 
                                        'last_team1':last_team1,'last_team2':last_team2, 'last_winner': last_winner})


@xframe_options_exempt
def prediction(request):
    if request.method == 'POST':
        data = {}
        data['runs'] = request.POST['runs']
        data['wickets'] = request.POST['wickets']
        data['overs'] = request.POST['overs']
        data['runs_last_5'] = request.POST['runs_last_5']
        data['wickets_last_5'] = request.POST['wickets_last_5']
        data['striker'] = request.POST['striker']
        data['non-striker'] = request.POST['non-striker']
        data['bat_team'] = request.POST['bat_team']
        data['bowl_team'] = request.POST['bowl_team']

        response=requests.post(url=f'{ROOT}/api/predict_score', data=data).json()
        
        if response['status']=='success':
            predicted_score=response['data']['predicted_score']
            # return redirect(result, predicted_score=predicted_score)
            return render(request, 'result.html', {'status':'success', 'predicted_score': predicted_score})
        else:
            # return redirect(result, predicted_score=0)
            return render(request, 'result.html', {'status':'failed'})
    else:
        return render(request, 'prediction.html')


def info(request):
    return render(request,'info.html')


def visualization(request):
    return render(request, 'visualization.html')

# def result(request, predicted_score):
#     if predicted_score != 0:
#         return render(request, 'result.html', {'status':'success', 'predicted_score': predicted_score})
#     else:
#         return render(request, 'result.html', {'status':'failed'})

def call_func(request):
    Schedule.load_schedule()
    return HttpResponse()

def schedule(request):
    schedule_all = Schedule.objects.all()

    for match in schedule_all:
        match.date=str(match.new_date)
        match.time=match.time.split(' ')[1]
    return render(request, 'schedule.html',{'schedule':schedule_all})

def about(request):
    return render(request, 'about.html')

def match(request):
    schedule_all = Schedule.objects.all()

    for key, schedule in enumerate(schedule_all, start=1):
        if key<=56:
            schedule.team1_abr=schedule.team1.split(' ')[-1][1:-1]
            schedule.team2_abr=schedule.team2.split(' ')[-1][1:-1]
        else:
            schedule.team1_abr=schedule.team1
            schedule.team2_abr=schedule.team2

    return render(request,'match.html',{'schedule':schedule_all})


def points_table(request):
    predicted_points = PointsTable.objects.order_by('-points')
    original_points = OriginalPointsTable.objects.order_by('-points', '-nrr')
    return render(request, 'points.html',{'predicted_points':predicted_points, 'original_points': original_points})

def qualifiers(request):
    schedule_all = Schedule.objects.all()[56:]
    return render(request,'qualifier.html',{'schedule':schedule_all})


def convert_to_format(dict):
    key_list = []
    for key in dict.keys():
        key_list.append(key)

    value_list = list(dict.values())

    data_dict = {}
    data_dict['keys'] = key_list
    data_dict['values'] = value_list
    return data_dict

def batsman():
    sql="SELECT batsman, SUM(batsman_runs) as sum FROM deliveries GROUP BY batsman ORDER BY sum DESC LIMIT 15"
    data = execute_query(sql)
    data_dict = {j[0]:int(j[1]) for j in data}
    return data_dict

def bowler():
    sql = "SELECT bowler, COUNT(*) FROM deliveries WHERE is_wicket=1 AND dismissal_kind!='run out' GROUP BY bowler ORDER BY `COUNT(*)` DESC LIMIT 15"
    data=execute_query(sql)
    data_dict = {j[0]:j[1] for j in data}
    return data_dict

def stats(request):
    runs = batsman()
    keys = []

    for key in runs.keys():
        keys.append(key)
    
    values = list(runs.values())
    runs = zip(keys,values)
    
    wickets = bowler()
    keys_2 = []
    
    for key in wickets.keys():
        keys_2.append(key)

    values_2 = list(wickets.values())
    wicket = zip(keys_2,values_2)
    return render(request, 'stats.html',{'runs':runs,'wicket':wicket})

def log(request, ip):
    print(ip)
    with open('log.txt', 'a') as log_file:
        log_file.write(ip+'\n')
    
    return HttpResponse()
