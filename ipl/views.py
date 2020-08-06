from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests

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

        response=requests.post(url='http://localhost:8000/api/predict-score', data=data).json()
        
        if response['status']=='success':
            predicted_score=response['data']['predicted_score']
            # return redirect(result, predicted_score=predicted_score)
            return render(request, 'result.html', {'status':'success', 'predicted_score': predicted_score})
        else:
            # return redirect(result, predicted_score=0)
            return render(request, 'result.html', {'status':'failed'})
    else:
        return render(request, 'prediction.html')


# def result(request, predicted_score):
#     if predicted_score != 0:
#         return render(request, 'result.html', {'status':'success', 'predicted_score': predicted_score})
#     else:
#         return render(request, 'result.html', {'status':'failed'})