from django.db import models
from pandas.core.algorithms import mode
# Create your models here.


class User(models.Model):
    uid=models.CharField(max_length=200,unique=True,blank=False,primary_key=True)
    name=models.CharField(max_length=100,default="")
    image=models.CharField(max_length=10000,default="")
    
    def __str__(self):
        return f"{self.name}" if len(self.name)>0 else f"{self.uid}"


class DailyScore(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    totalPoints=models.IntegerField(default=0)
    timeTaken=models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.name} scored {self.totalPoints} in {self.timeTaken} seconds"
    
    class Meta:
        ordering = ['-totalPoints','timeTaken']


class Question(models.Model):
    question=models.CharField(max_length=1000)
    opt1=models.CharField(max_length=500)
    opt2=models.CharField(max_length=500)
    opt3=models.CharField(max_length=500)
    opt4=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    addedOn=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.question

class Tries(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    tries=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural="Tries"

    def __str__(self):
        return f"{self.user} has tried {self.tries} today"