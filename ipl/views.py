from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def prediction(request):
    if request.method == 'POST':
        runs = request.POST['runs']
        return render(request, 'prediction.html', {'new_runs': runs})
    else:
        return render(request, 'prediction.html')