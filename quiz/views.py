from .models import DailyScore, PracticeQuestions, Question, SponsoredAttempts, SponsoredQuestions, SponsoredScoreboard, Tries, User
from django.http import HttpRequest,JsonResponse,HttpResponseBadRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404

# Create your views here.


@csrf_exempt
def goc(request :HttpRequest):
    uid=request.POST.get('uid',False) 
    if(not uid):
        return HttpResponseBadRequest({'status':'MDR'})
    user,created=User.objects.get_or_create(uid=uid)
    if(created):
        user.name=request.POST.get('name',"")
        user.roll=request.POST.get('roll',"")
        user.save()
        return JsonResponse({'status':'NUC'})
    else:
        tmp= user.__dict__
        tmp.update({'status':"FEU"})
        tmp.pop('_state')
        return JsonResponse(tmp)



@csrf_exempt
def update(request :HttpRequest):

    uid=request.POST.get('uid',False) 
    image=request.POST.get('img',False)
    name=request.POST.get('name',False)
    roll=request.POST.get('roll',False)

    if(all((uid,name,image))):
        user=User.objects.get(uid=uid)
        user.name=name
        user.image=image

        if(roll):
            user.roll=roll
        if(name):
            user.name=name
        user.save()

        return JsonResponse({'status':'UPS'})
    else:
        return HttpResponseBadRequest(json.dumps({'status':'MDR'}))



@csrf_exempt
def practiceSubmit(request :HttpRequest):
    uid=request.POST.get('uid',False)
    total=request.POST.get('total',False)
    time=request.POST.get('time',False)

    print(uid,total,time)
    if(not all((uid,total,time))):
        return HttpResponseBadRequest({'status':'MDR'})
    user=User.objects.get(uid=uid)
    if(not user):
        return JsonResponse({'status':'UNF'})
    try:
        score=DailyScore.objects.create(user=user,totalPoints=total,timeTaken=time)
    except:
        return JsonResponse({'status':'AST'})

    return JsonResponse({'status':'PSS'})



def getLeaderBoard(request :HttpRequest):
    def f(x):
        nonlocal i
        i+=1
        return {'index': i ,'name':x.user.name,'image':x.user.image,'totalPoints':x.totalPoints,'timeTaken':x.timeTaken}
    
    i=0
    l=DailyScore.objects.all()[:10]
    return JsonResponse([ f(x) for x in l],safe=False)



def sponsoredLeaderBoard(request :HttpRequest):
    def f(x):
        nonlocal i
        i+=1
        return {'index': i ,'name':x.user.name,'image':x.user.image,'totalPoints':x.totalPoints,'timeTaken':x.timeTaken}
    
    i=0
    l=SponsoredScoreboard.objects.all()[:10]
    return JsonResponse([ f(x) for x in l],safe=False)



@csrf_exempt
def getQuestion(request: HttpRequest):
    uid=request.POST.get('uid',None)
    bid=request.POST.get('bid',1)
    user=User.objects.filter(uid=uid)
    if(not user.exists()):
        return JsonResponse({'status':'UNF'})
    if(DailyScore.objects.filter(user=user[0]).exists()):
        return JsonResponse({'status':'AST'})
    
    triesObj,created=Tries.objects.get_or_create(user=user[0])
    if(triesObj.tries>2):
        return JsonResponse({'status':'MRR'})
    
    triesObj.tries=triesObj.tries+1
    triesObj.save()
    questions= PracticeQuestions.objects.get(id=bid).question_set.order_by('?')[:10]
    qdictlist=[]
    for q in questions:
        qdictlist.append({"index": q.id,
         "question": q.question,
          "option_a": q.opt1, 
          "option_b": q.opt2, 
          "option_c": q.opt3, 
          "option_d": q.opt4,
          "answer": q.answer
          })
    
    return JsonResponse({'questions':qdictlist,'status':'ATA '})
	


@csrf_exempt
def uploadQuestions(request :HttpRequest):
    def parseQuestions(row):
        q,o1,o2,o3,o4,ans=row
        question,created=Question.objects.get_or_create(question=q,opt1=o1,opt2=o2,opt3=o3,opt4=o4,answer=ans)
        if(not created):
            message.append('ignored existing question '+q)

    
    file=request.FILES.get('questionsFile',False)
    message=[]
    if file==False:
        return JsonResponse({'status':'NFU'})
    elif file.name.strip().endswith("csv"):
        xlsx=False
    elif file.name.strip().endswith("xlsx"):
        xlsx=True
    else:
        return JsonResponse({'status':'BFE'})
    
    import pandas
    df=pandas.read_csv(file) if not xlsx else pandas.read_excel(file)
    try:
        df.apply(parseQuestions,axis=1) 
        message={'status':'QUS'} if len(message)==0 else {'status':'QUS','messages':message}
        return JsonResponse(message)
    except Exception as e:
        return JsonResponse({'status':'ERR','error':str(e)})


    


@csrf_exempt
def getSponsoredQuestion(request: HttpRequest):

    uid=request.POST.get('uid',None)
    exCode=request.POST.get('code','')
    
    from datetime import datetime

    user=User.objects.filter(uid=uid)

    print(dir(SponsoredQuestions.objects.all()[0]))
    print(exCode)

    sponsorObject=SponsoredQuestions.objects.filter(examCode=exCode)
    if(sponsorObject):
        sponsorObject=sponsorObject[0]
    else:
        return JsonResponse({'status':'ENF'})
    
    if(not user.exists()):
        return JsonResponse({'status':'UNF'})

    if(sponsorObject.startTime.timestamp()>datetime.now().timestamp()):
        return JsonResponse({'status':'NSY','startTime':sponsorObject.startTime.timestamp()//1})
    
    if(sponsorObject.endTime.timestamp()<datetime.now().timestamp()):
        return JsonResponse({'status':'FIN','endTime':sponsorObject.endTime.timestamp()//1})

    if(SponsoredScoreboard.objects.filter(user=user[0],sponsor_id=sponsorObject.id).exists()):
        return JsonResponse({'status':'AST'})
    
    triesObj,created=SponsoredAttempts.objects.get_or_create(user=user[0],sponsor_id=sponsorObject.id)
    
    if(triesObj.tries>2):
        return JsonResponse({'status':'MRR'})
    
    triesObj.tries=triesObj.tries+1
    triesObj.save()
    
    questions=sponsorObject.question_set.all()
    qdictlist=[]

    for q in questions:
        qdictlist.append({"index": q.id,
         "question": q.question,
          "option_a": q.opt1, 
          "option_b": q.opt2, 
          "option_c": q.opt3, 
          "option_d": q.opt4,
          #"answer": q.answer
          })
    
    return JsonResponse({'questions':qdictlist,
            'status':'ATA',
            'starttime':str(sponsorObject.startTime.timestamp()),
            'endtime':str(sponsorObject.endTime.timestamp()),
            'name':sponsorObject.name,
            'branch':sponsorObject.branch,
            'examCode':sponsorObject.examCode,
            })

	



@csrf_exempt
def sponsoredSubmit(request :HttpRequest):

    from ErpCrawler.settings import BASE_DIR

    with open(str(BASE_DIR)+'/submitTest','w+') as f:
        f.write('\n'*4)
        json.dump(request.POST,f)
        f.close()


    uid=request.POST.get('uid',False)
    total=request.POST.get('total',False)
    branch=request.POST.get('branch',False)
    section=request.POST.get('section',False)
    year=request.POST.get('year',False)
    exCode=request.POST.get('code',False)
    
    time=request.POST.get('time',False)

    print(uid,total,time)

    if(not all((uid,total,time))):
        return HttpResponseBadRequest({'status':'MDR'})


    user=User.objects.get(uid=uid)

    if(not user):
        return JsonResponse({'status':'UNF'})

    try:
        score=DailyScore.objects.create(user=user,totalPoints=total,timeTaken=time)
    except:
        return JsonResponse({'status':'AST'})

    return JsonResponse({'status':'PSS'})
