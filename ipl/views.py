from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def prediction(request):
    if request.method == 'POST':
        runs = request.POST['runs']
        wickets = request.POST['wickets']
        runs_last_5 = request.POST['runs_last_5']
        wickets_last_5 = request.POST['wickets_last_5']
        striker = request.POST['striker']
        non_striker = request.POST['non_striker']
        bat_team = request.POST['bat_team']
        bowl_team = request.POST['bowl_team']
        return render(request, 'prediction.html', {'runs': runs, 'wickets':wickets, 'runs_last_5':runs_last_5,
                                                   'wickets_last_5':wickets_last_5,'striker':striker,'non_striker':non_striker,
                                                   'bat_team':bat_team,'bowl_team':bowl_team})
    else:
        return render(request, 'prediction.html')