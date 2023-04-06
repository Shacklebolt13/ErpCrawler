from quiz import models
from datetime import datetime
from ErpCrawler.settings import BASE_DIR


def refresh():
    open(
        str(BASE_DIR)
        + "/schedules/ran_at_"
        + datetime.now().strftime("%H_%M_%S_%d_%m_%y"),
        "w",
    ).close()
    models.DailyScore.objects.all().delete()
    models.Tries.objects.all().delete()


# 15
# ranjit@1983
