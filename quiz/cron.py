from . import models
from datetime import datetime
def refreshdailyLeaderboard():
    open('./schedules/ran_at_'+ datetime.now().strftime('%H_%M_%S_%d_%m_%y'),'w').close()
    models.DailyScore.objects.all().delete()
    models.Tries.objects.all().delete()
   
    