from django.db import models
from bs4 import BeautifulSoup
import requests
import datetime 
import time

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
    qualifier_type=models.TextField(null=True)
    team1 = models.TextField()
    team2 = models.TextField()
    date = models.TextField()
    new_date = models.DateField()
    day = models.TextField()
    time = models.TextField()
    city = models.TextField()
    predicted_winner=models.TextField(null=True)
    original_winner=models.TextField(null=True)

    def load_schedule():
        
        source = requests.get("https://www.icccricketschedule.com/vivo-ipl-2020-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/").text
        soup = BeautifulSoup(source,'lxml')

        table = soup.find('table')

        matches_rows = table.find_all('tr')
        matches_rows=matches_rows[1:]

        for matches in matches_rows:

            new = matches.find_all('td')
            new = list(map(lambda x:str(x.text).replace(',', ''), new))
            print(new[0])

            matches = Schedule()
            
            format = '%d %B %Y' # The format 
            datetime_str = datetime.datetime.strptime(new[2], format) 

            team = new[1]

            team1=team.split('Vs')[0]
            team2=team.split('Vs')[1]

            matches.team1 = team1.strip()
            matches.team2 = team2.strip()
            matches.date = new[2]
            matches.day = new[3]
            matches.new_date = datetime_str.strftime('%Y-%m-%d')
            matches.time = new[4]
            matches.city = new[6]

            matches.save()


class PointsTable(models.Model):

    team = models.TextField()
    played = models.IntegerField()
    won = models.IntegerField()
    lost = models.IntegerField()
    points = models.IntegerField()

class OriginalPointsTable(models.Model):

    team = models.TextField()
    played = models.IntegerField()
    won = models.IntegerField()
    lost = models.IntegerField()
    points = models.IntegerField()
    nrr = models.DecimalField(max_digits=5, decimal_places=2)

    def load_table():
        link = "https://www.iplt20.com/points-table/2020"
        soup = BeautifulSoup(requests.get(link).text, 'lxml')

        table = soup.find('table', class_='standings-table')
        rows = table.findAll('tr')[1:]

        for id, row in enumerate(rows, start=1):
            cols=row.findAll('td')
            record = OriginalPointsTable()
            record.id=id
            record.team=cols[1].text.strip().split('\n')[0]
            record.played=cols[2].text
            record.won=cols[3].text
            record.lost=cols[4].text
            record.points=cols[10].text
            record.nrr=cols[7].text
            record.save()