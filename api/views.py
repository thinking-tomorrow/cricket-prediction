from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def predict_score(request):
    return JsonResponse({'status': 'success', 'data':{'predicted-socre': 200}})