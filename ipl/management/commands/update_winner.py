from django.core.management.base import BaseCommand, CommandError
from ipl.models import Schedule
from bs4 import BeautifulSoup
import datetime
import requests
import pytz

class Command(BaseCommand):

    def handle(self, *args, **options):
        link = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"
        soup = BeautifulSoup(requests.get(link).text, 'lxml')

        tz=pytz.timezone('Asia/Kolkata')
        yesterday=datetime.datetime.now(tz)-datetime.timedelta(days=1)
        matches=Schedule.objects.filter(new_date=yesterday)
        
        for match in matches:
            match_soup = soup.findAll('div', class_='cb-series-matches')[match.id-1]
            original_winner=' '.join(match_soup.findAll('div')[2].find('div').findAll('a')[1].text.split(' ')[0:-4])
            match.original_winer=original_winner
            match.save()