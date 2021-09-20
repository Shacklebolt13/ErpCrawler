from . import models
from datetime import datetime
def refreshdailyLeaderboard():
    models.DailyScore.objects.all().delete()
    open('schedules/ran_at_%H_%M_%S_%d_%m_%y','r').close()
    
