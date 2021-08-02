from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from . import erpCrawler
from scrapyscript import Job,Processor
import json

def runScraper(request: HttpRequest):
    u=request.GET.get('username',False)
    p=request.GET.get('password',False)
    print(u,p)
    if((not u) or (not p)):
        return HttpResponseBadRequest("must pass username and password as get fields")
    getRes=Job(erpCrawler.ErpCrawler,u=u,p=p)
    process=Processor(settings=None)
    ans=process.run(getRes)
    
    return HttpResponse(json.dumps(ans,indent=4))