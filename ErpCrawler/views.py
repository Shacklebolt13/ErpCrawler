from ErpCrawler import settings
from ErpCrawler import ttCrawler
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from . import erpCrawler,ResCrawler
from scrapyscript import Job,Processor
import json
import random
from cryptography.fernet import Fernet
from .helpers import EmailThread
from django.views.decorators.csrf import csrf_exempt

def runAttScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(erpCrawler.ErpCrawler,u=u,p=p)
    process=Processor(settings=None)
    ans=process.run(getRes)
    
    return HttpResponse(json.dumps(ans))


def runTTScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(ttCrawler.TTcrawler,u=u,p=p)
    process=Processor(settings=None)
    ans=process.run(getRes)
    
    return HttpResponse(json.dumps(ans))

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
    return HttpResponse(json.dumps(ans))


@csrf_exempt
def sendMail(request: HttpResponse):
    mail=request.POST.get('mail',False)
    key=request.POST.get('key',False)
    print(mail,key)
    if(not mail or not key):
        return HttpResponse('Pass mailId and key')
    otp=''
    while len(otp)<6:
        otp+=f"{random.randint(0,9)}"
    
    msg=f'The Otp For Verification Of Your Email Is: {otp}'
    print(msg)
    EmailThread("Otp For Verification",msg,[mail]).start()
    if(key!=settings.MAIL_KEY):
        return HttpResponse('Wrong key')
    key=Fernet.generate_key()
    fernet=Fernet(key)
    enc=fernet.encrypt(otp.encode())
    frm={'encoded': f"{str(key,'utf-8')}{str(enc,'utf-8')}",'otp':f'{otp}'}
    return HttpResponse(json.dumps(frm))

