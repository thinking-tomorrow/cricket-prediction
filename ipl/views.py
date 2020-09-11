from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from .models import Schedule, PointsTable, OriginalPointsTable
from django.views.decorators.clickjacking import xframe_options_exempt

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
        matches.city = new[5]

        matches.save()        

def home(request):
    return render(request, 'home.html')

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

        response=requests.post(url='http://localhost:8000/api/predict_score', data=data).json()
        
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
    return render(request, 'schedule.html',{'schedule':schedule_all})

def about(request):
    return render(request, 'about.html')

def match(request):
    schedule_all = Schedule.objects.all()

    for schedule in schedule_all:
        schedule.team1_abr=schedule.team1.split(' ')[-1][1:-1]
        schedule.team2_abr=schedule.team2.split(' ')[-1][1:-1]

    return render(request,'match.html',{'schedule':schedule_all})


def points_table(request):
    predicted_points = PointsTable.objects.order_by('-points')
    original_points = OriginalPointsTable.objects.order_by('points', 'nrr')
    return render(request, 'points.html',{'predicted_points':predicted_points, 'original_points': original_points})

def qualifiers(request):
    schedule_all = Schedule.objects.all()[56:]
    return render(request,'qualifier.html',{'schedule':schedule_all})