from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from ipl.models import Schedule, PointsTable, OriginalPointsTable

class Command(BaseCommand):

    def handle(self, *args, **options):
        PointsTable.objects.all().delete()
        table = Schedule.objects.values('predicted_winner').annotate(the_count=Count('predicted_winner')).filter(id__lte=56)

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
        
        OriginalPointsTable.objects.all().delete()
        OriginalPointsTable.load_table()