from django.db import models
from bs4 import BeautifulSoup
import requests

class Matches(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.TextField()
    date = models.DateField()
    team1 = models.TextField()
    team2 = models.TextField()
    toss_winner = models.TextField()
    toss_decision = models.TextField()
    result = models.TextField()
    dl_applied = models.IntegerField()
    winner = models.TextField()
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    venue = models.TextField()
    mom = models.TextField()
    
class Schedule(models.Model):
    team1 = models.TextField()
    team2 = models.TextField()
    date = models.TextField()
    day = models.TextField()
    time = models.TextField()
    city = models.TextField()

    def load_schedule():
        
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
            
            team = new[1]

            team1=team.split('Vs')[0]
            team2=team.split('Vs')[1]

            matches.team1 = team1.strip()
            matches.team2 = team2.strip()
            matches.date = new[2]
            matches.day = new[3]
            matches.time = new[4]
            matches.city = new[5]

            matches.save()
