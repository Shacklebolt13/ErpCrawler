from django.http.response import HttpResponse
from .models import DailyScore, User, models
from django.http import HttpRequest,JsonResponse,HttpResponseBadRequest,HttpResponse
# Create your views here.
def goc(request :HttpRequest):
    uid=request.GET.get('uid',False) 
    if(not uid):
        return HttpResponseBadRequest({'status':'MDR'})
    user,created=models.User.objects.get_or_create(uid=uid)
    if(created):
        user.save()
        return JsonResponse({'status':'NUC'})
    else:
        tmp= user.__dict__
        tmp.update({'status':"FEU"})
        tmp.pop('_state')
        return JsonResponse(tmp)


def update(request :HttpRequest):
    uid=request.GET.get('uid',False) 
    name=request.GET.get('name',False)
    image=request.GET.get('img',False)
    if(all((uid,name,image))):
        user=User.objects.get(uid=uid)
        user.name=name
        user.image=image
        return JsonResponse({'status':'UPS'})
    else:
        return HttpResponseBadRequest({'status':'MDR'})

def practiceSubmit(request :HttpRequest):
    uid=request.GET.get('uid',False)
    total=request.GET.get('total',False)
    time=request.GET.get('time',False)

    if(not all((uid,total,time))):
        return HttpResponseBadRequest({'status':'MDR'})
    user=User.objects.get(uid=uid)
    if(not user):
        return JsonResponse({'status':'UNF'})

    score=DailyScore.objects.create(user=user,totalPoints=total,timeTaken=time)

    return JsonResponse({'status':'PSS'})


def getLeaderBoard(request :HttpRequest):

    l=DailyScore.objects.all()
    return JsonResponse([{'name':x.user.name,'image':x.user.image,'totalPoints':x.totalPoints,'timeTaken':x.timeTaken} for x in l],safe=False)

