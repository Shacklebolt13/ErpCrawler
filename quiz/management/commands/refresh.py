from django.core.management.base import BaseCommand, CommandError
from quiz import models
from datetime import datetime
import pytz
from ErpCrawler.settings import BASE_DIR


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        open(
            str(BASE_DIR)
            + "/schedules/ran_at_"
            + datetime.now().strftime("%H_%M_%S_%d_%m_%y"),
            "w",
        ).close()
        models.DailyScore.objects.all().delete()
        models.Tries.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully ran at "
                + datetime.now().strftime("%H:%M:%S %d/%m/%y")
                + " "
                + datetime.now(pytz.utc).strftime("%H:%M:%S %d/%m/%y")
            )
        )


# 15
# ranjit@1983
