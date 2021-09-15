from .models import DailyScore, User
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

    l=DailyScore.objects.all()[:10]
    return JsonResponse([{'name':x.user.name,'image':x.user.image,'totalPoints':x.totalPoints,'timeTaken':x.timeTaken} for x in l],safe=False)


def getQuestion(request: HttpRequest):
    uid=request.GET.get('uid',None)
    if(DailyScore.objects.filter(user=uid).exists()):
        return JsonResponse({'status':'AST'})
    return JsonResponse({'questions':[{"index": 1, "question": "How to delete a directory in Linux?", "option_a": "ls", "option_b": "delete", "option_c": "remove", "option_d": "rmdir", "answer": "delete"}]*10,'status':'ATA '})