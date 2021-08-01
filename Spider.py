import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import logging
import json
from scrapy.http.response.html import HtmlResponse


class spiderForAttendance(scrapy.Spider):
    name='spiderForAttendance'
    attendanceSite='http://www.gandhionline.in/BEESERP/Login.aspx'
    btnNext= 'Next'
    btnSubmit='Submit'
    txtUserName='u'
    txtPassword='p'
    __LASTFOCUS=""
    __EVENTTARGET=""
    __EVENTARGUMENT=""
    start_urls=[attendanceSite]
    data :dict
    data={}
    returnJson={}


    def __init__(self,u='u',p='p'):
        self.txtUserName=u
        self.txtPassword=p
        super(spiderForAttendance,self).__init__()




    def parse(self,response : HtmlResponse):
        self.getBasicData(response)
        self.data.update({'txtUserName' : self.txtUserName,'btnNext': self.btnNext })
        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.loginWithPassword)



    def loginWithPassword(self,response : HtmlResponse):
        self.getBasicData(response)
        self.data.update({'txtPassword' : self.txtPassword,'btnSubmit' : self.btnSubmit})
        print('__REACHED__')
        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.gotoSemMarksPage)


    def getBasicData(self,response,reset=False):
        self.data={} if reset else self.data
        self.__VIEWSTATEGENERATOR=response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').extract_first()
        self.__EVENTVALIDATION=response.css('input[name="__EVENTVALIDATION"]::attr(value)').extract_first()
        self.__VIEWSTATE=response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()
        self.data={'__VIEWSTATEGENERATOR' : self.__VIEWSTATEGENERATOR,
                   '__EVENTVALIDATION' : self.__EVENTVALIDATION,
                   '__VIEWSTATE' : self.__VIEWSTATE,
                   '__LASTFOCUS' : self.__LASTFOCUS,
                   '__EVENTTARGET' : self.__EVENTTARGET,
                   '__EVENTARGUMENT' : self.__EVENTARGUMENT,
                  }

    def showOutHtml(self,response : HtmlResponse):
        file=open('view.html','w+b')
        file.write(response.body)
        file.close


    def gotoSemMarksPage(self,response : HtmlResponse):
        self.attendanceDetails(response)
        #TODO get it into a json
        yield scrapy.FormRequest(method='GET',url='https://www.gandhionline.in/BEESERP/StudentLogin/Student/OverallMarksSemwise.aspx',callback=self.getMarks)
        

    def getMarks(self,response : HtmlResponse):
        self.percentageDetails(response)
        self.getBasicData(response,reset=True)
        self.data.pop("__EVENTVALIDATION")
        crystalState=response.css('input[name="__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1"]::attr(value)').extract_first()
        self.data.update({'ctl00$cpStud$btn1' : 'I SEMESTER','__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1':crystalState})
        yield scrapy.FormRequest(url=r'https://www.gandhionline.in/BEESERP/StudentLogin/Student/OverallMarksSemwise.aspx',formdata=self.data,callback=self.sem1Marks)



    def sem1Marks(self,response):
        self.showOutHtml(response)
        pass







    def attendanceDetails(self,response : HtmlResponse):
        att=response.xpath('//*[@id="ctl00_cpStud_lblTotalPercentage"]/b/font').extract_first()
        print(att)
        self.att=float(att[att.index('>')+1:att.index('%')])
        print('\n\n\n\n\n\n YOUR ATTENDANCE IS: ',self.att,'\n\n\n\n\n\n')



    def percentageDetails(self,response : HtmlResponse):
        pass









if(len(sys.argv)>=3 and sys.argv[0].lower()!='runspider'):
    print(sys.argv[0])
    txtUserName=sys.argv[1]
    txtPassword=sys.argv[2]

    spider=spiderForAttendance()
    spider.txtUserName=txtUserName
    spider.txtPassword=txtPassword

    process = CrawlerProcess(settings={'level': logging.CRITICAL})
    process.crawl(spiderForAttendance,u=txtUserName,p=txtPassword)
    process.start()
    #os.popen(f'scrapy runspider {sys.argv[0]} -a u={txtUserName} -a p={txtPassword} > NUL')
elif(sys.argv[0].lower()!='runspider'):
    print("syntax: Spider.py username password")
    exit()
else:
    pass
