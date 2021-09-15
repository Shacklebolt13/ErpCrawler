from django.db import models
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
    answer=models.IntegerField(choices=((1,"OPT1"),(2,"OPT2"),(3,"OPT3"),(4,"OPT4")))

    def __str__(self):
        return self.question
