from django.db import models

class Matches(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.TextField()
    date = models.DateField()
    
    
