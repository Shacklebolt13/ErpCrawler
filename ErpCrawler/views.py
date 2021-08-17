from ErpCrawler import ttCrawler
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from . import erpCrawler,ResCrawler
from scrapyscript import Job,Processor
import json

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



def sendMail(self,response: HtmlResponse):
    pass
        