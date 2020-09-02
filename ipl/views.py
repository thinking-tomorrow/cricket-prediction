from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from .models import Schedule

def scrape_schedule():

    source = requests.get("https://www.icccricketschedule.com/vivo-ipl-2020-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/").text
    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')

    '''for matches in table:

        rows = matches.find_all('td')
        print(rows[1])'''

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
# Create your views here.
def home(request):
    return render(request, 'home.html')

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


#Schedule.objects.all().delete()

def schedule(request):
    schedule_all = Schedule.objects.all()
    # schedule_all = map(lambda x:print(x.team1), schedule_all)
    return render(request, 'schedule.html',{'schedule':schedule_all})