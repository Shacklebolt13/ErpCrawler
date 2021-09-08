from ErpCrawler import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from . import resultsCrawler,attendancePageCrawler,timeTableCrawler,bioCrawler,dpCrawler
import json
import random
from .helpers import EmailThread, encryptResp
from django.views.decorators.csrf import csrf_exempt
from . import emailpreview

def runAttScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    a=attendancePageCrawler.attendancePageCrawler(u,p)
    return HttpResponse(json.dumps( a if  isinstance(a,list) else [a]))


def runDpScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    return HttpResponse(json.dumps(dpCrawler.dpCrawler(u,p)))


def runTTScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    
    return HttpResponse(json.dumps([timeTableCrawler.timeTableCrawler(u,p)]))



def runBioScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    t=request.GET.get('type','dict')
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    
    return HttpResponse(json.dumps(bioCrawler.bioCrawler(u,p,t)))

def runResScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    c=request.GET.get('cookie',False)
    s=int(request.GET.get('semester',False))
    print(u,p,c,s)
    if((not s) or(not c) or(not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    print(c)
    return HttpResponse(json.dumps([resultsCrawler.resultsCrawler(u,p,s,dict(map(lambda x : x.split('='),c.split(';'))))]))


@csrf_exempt
def sendMail(request: HttpResponse):
    mail=request.POST.get('mail',False)
    key=request.POST.get('key',False)

    # print(mail,key)
    
    if(not mail or not key):
        return HttpResponseBadRequest("must pass mail and key as get fields")
    
    
    otp=''
    while len(otp)<6:
        otp+=f"{random.randint(0,9)}"
    
    #signature='GIETU Official App Team<br><img src="http://www.gandhionline.in/BEESERP/Images/header.jpg">'
    #msg=f'Dated: {time} <br>The Otp For Verification Of Your Email Is: {otp} <br><br>{signature}'
    # print(msg)
    if(key!=settings.MAIL_KEY):
        return HttpResponse('Wrong key')
    
    EmailThread("Otp For Verification",emailpreview.message(otp,mail),[mail]).start()
    #print(otp)
    enc,dummy=encryptResp(otp,fuzzLen=9,dummyLen=6,dummy=True,onlyDigit=True)

    frm={'encoded':enc,'otpKey':f'{dummy}'}
    return HttpResponse(json.dumps(frm))

