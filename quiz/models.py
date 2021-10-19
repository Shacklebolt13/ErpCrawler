from django.db import models
import base64
from ErpCrawler.settings import BASE_DIR

# Create your models here.
defImg= base64.b64encode(open(str(BASE_DIR)+'/quiz/static/quiz/defImg.jpg','rb').read()).decode()


class User(models.Model):
    uid=models.CharField(max_length=200,unique=True,blank=False,primary_key=True)
    name=models.CharField(max_length=100,default="")
    roll=models.CharField(max_length=20,default="")

    image=models.CharField(max_length=100000,default=defImg,null=True)
    
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


class PracticeQuestions(models.Model):
    
    class Meta:
        verbose_name_plural="Practice Branch"

    branch=models.CharField(max_length=10)

    def __str__(self):
        return self.branch



class SponsoredQuestions(models.Model):
    class Meta:
        verbose_name_plural="Sponsored Details"

    branch=models.CharField(max_length=10,null="")
    name=models.CharField(max_length=64,null="")
    timePeriod=models.IntegerField(default=60)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    examCode=models.CharField(max_length=30,default='')

    
    def __str__(self):
        ts=self.startTime.timestamp()//1
        return f"{self.examCode} : {self.name} exam ({self.branch}) for {self.timePeriod} mins at {ts}"

   
    
class SponsoredScoreboard(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    totalPoints=models.IntegerField(default=0)
    branch=models.CharField(max_length=10,blank=True)
    section=models.CharField(max_length=5,null=True)
    year=models.IntegerField(default=19)
    sponsor=models.ForeignKey(SponsoredQuestions,on_delete=models.DO_NOTHING)
    semester=models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.name} scored {self.totalPoints} "
    
    class Meta:
        ordering = ['-totalPoints']


class SponsoredAttempts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tries=models.IntegerField(default=0)
    sponsor=models.ForeignKey(SponsoredQuestions,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural="Sponsored Tries"

    def __str__(self):
        return f"{self.user} has tried {self.tries} times today"




class Question(models.Model):
    question=models.CharField(max_length=1000)
    opt1=models.CharField(max_length=500)
    opt2=models.CharField(max_length=500)
    opt3=models.CharField(max_length=500)
    opt4=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    addedOn=models.DateTimeField(auto_now_add=True,blank=True)
    practiceBranch=models.ForeignKey(PracticeQuestions,null=True,on_delete=models.RESTRICT,blank=True)
    sponsorship=models.ForeignKey(SponsoredQuestions,null=True,on_delete=models.RESTRICT,blank=True)

    def __str__(self):
        return self.question

class Tries(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    tries=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural="Tries"

    def __str__(self):
        return f"{self.user} has tried {self.tries} times today"
