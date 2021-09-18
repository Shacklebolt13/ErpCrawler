from . import models

def refreshdailyLeaderboard():
    models.DailyScore.objects.all().delete()