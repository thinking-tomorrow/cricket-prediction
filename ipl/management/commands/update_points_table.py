from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from ipl.models import Schedule, PointsTable

class Command(BaseCommand):

    def handle(self, *args, **options):
        table = Schedule.objects.values('predicted_winner').annotate(the_count=Count('predicted_winner'))

        for team in table:
            team_points=PointsTable()
            
            name=team['predicted_winner']
            won=team['the_count']

            team_points.played=14
            team_points.lost=14-won
            team_points.won=won
            team_points.team=name
            team_points.points=won*2
            team_points.save()