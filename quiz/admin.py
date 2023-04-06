from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.DailyScore)
admin.site.register(models.Question)
admin.site.register(models.Tries)
admin.site.register(models.SponsoredAttempts)
admin.site.register(models.SponsoredQuestions)
admin.site.register(models.SponsoredScoreboard)
admin.site.register(models.PracticeQuestions)
