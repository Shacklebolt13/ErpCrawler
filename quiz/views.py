from .models import DailyScore, Question, Tries, User
from django.http import HttpRequest,JsonResponse,HttpResponseBadRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def goc(request :HttpRequest):
    uid=request.POST.get('uid',False) 
    if(not uid):
        return HttpResponseBadRequest({'status':'MDR'})
    user,created=User.objects.get_or_create(uid=uid)
    if(created):
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
    name=request.POST.get('name',False)
    image=request.POST.get('img',False)
    if(all((uid,name,image))):
        user=User.objects.get(uid=uid)
        user.name=name
        user.image=image
        user.save()
        return JsonResponse({'status':'UPS'})
    else:
        return HttpResponseBadRequest(json.dumps({'status':'MDR'}))

@csrf_exempt
def practiceSubmit(request :HttpRequest):
    uid=request.POST.get('uid',False)
    total=request.POST.get('total',False)
    time=request.POST.get('time',False)

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

@csrf_exempt
def getQuestion(request: HttpRequest):
    uid=request.POST.get('uid',None)
    
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
    questions=Question.objects.order_by('?')[:10]
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

    
    file=request.FILES.get('questionsCSV',False)
    message=[]
    if file==False:
        return JsonResponse({'status':'NFU'})
    elif not file.name.strip().endswith("csv"):
        return JsonResponse({'status':'BFE'})
    
    import pandas
    df=pandas.read_csv(file)
    try:
        df.apply(parseQuestions,axis=1) 
        message={'status':'QUS'} if len(message)==0 else {'status':'QUS','messages':message}
        return JsonResponse(message)
    except Exception as e:
        return JsonResponse({'status':'ERR','error':str(e)})


    
    
    