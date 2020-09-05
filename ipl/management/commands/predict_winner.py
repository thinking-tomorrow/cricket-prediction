from django.core.management.base import BaseCommand, CommandError

import ast
import json
import requests
from ipl.models import Schedule

class Command(BaseCommand):

    def handle(self, *args, **options):
        matches = Schedule.objects.all()

        predicted_winners=ast.literal_eval(requests.get('http://127.0.0.1:8000/api/winner').json()['data'])
        
        for key, match in enumerate(matches):
            match.predicted_winner=predicted_winners[key]
            match.save()
        