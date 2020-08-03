from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def predict_score(request):
    # if all(name in grades for name in students):
    keys = ['runs', 'wickets', 'runs_last_5', 'wickets_last_5', 'striker', 'non-striker', 'bat_team', 'bowl_team']
    if all(key in request.POST for key in keys):
        return JsonResponse({'status': 'success', 'data':{'predicted-socre': 200}})
    else:
        return JsonResponse({'status': 'failed'})