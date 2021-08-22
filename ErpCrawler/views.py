import base64
from ErpCrawler import settings
from ErpCrawler import ttCrawler
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest,JsonResponse
from . import erpCrawler,ResCrawler
from scrapyscript import Job,Processor
import os
import random
from cryptography.fernet import Fernet
from .helpers import EmailThread, encryptResp
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ErpCrawler import helpers



def runAttScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(erpCrawler.ErpCrawler,u=u,p=p)
    process=Processor(settings=None)
    ans=process.run(getRes)
    return JsonResponse(ans[0],safe=False)


def runTTScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(ttCrawler.TTcrawler,u=u,p=p)
    process=Processor(settings=None)
    ans=process.run(getRes)
    
    return JsonResponse(ans[0],safe=False)

def runResScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    c=request.GET.get('cookie',False)
    s=int(request.GET.get('semester',False))
    print(u,p,c,s)
    if((not s) or(not c) or(not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(ResCrawler.ResCrawler,u=u,p=p,s=s,c=c)
    process=Processor(settings=None)
    ans=process.run(getRes)
    return JsonResponse(ans[0] if len(ans)>0 else ans,safe=False)


@csrf_exempt
def sendMail(request: HttpResponse):
    mail=request.POST.get('mail',False)
    key=request.POST.get('key',False)
    password=request.POST.get('pass',False)
    
    # print(mail,key)
    
    if(not mail or not key):
        return HttpResponseBadRequest("must pass mail and key as get fields")
    
    
    otp=''
    while len(otp)<6:
        otp+=f"{random.randint(0,9)}"
    msg=f'The Otp For Verification Of Your Email Is: {otp}'
    # print(msg)
    if(key!=settings.MAIL_KEY):
        return JsonResponse({'error':'Wrong key'})
    
    EmailThread("Otp For Verification",msg,[mail]).start()

    enc=encryptResp(password,otp)
    
    frm={'encoded': f"{str(key,'utf-8')}{str(enc,'utf-8')}",'otp':f'{otp}'}
    return JsonResponse(frm)

