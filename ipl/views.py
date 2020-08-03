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
        return render(request, 'prediction.html', {'new_runs': runs})
    else:
        return render(request, 'prediction.html')