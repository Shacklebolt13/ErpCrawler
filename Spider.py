import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import logging

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

    def __init__(self,u='u',p='p'):
        self.txtUserName=u
        self.txtPassword=p
        super(spiderForAttendance,self).__init__()

    def parse(self,response):
        self.__VIEWSTATEGENERATOR=response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').extract_first()
        self.__EVENTVALIDATION=response.css('input[name="__EVENTVALIDATION"]::attr(value)').extract_first()
        self.__VIEWSTATE=response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()

        self.data={'__VIEWSTATEGENERATOR' : self.__VIEWSTATEGENERATOR,
                   '__EVENTVALIDATION' : self.__EVENTVALIDATION,
                   '__VIEWSTATE' : self.__VIEWSTATE,
                   '__LASTFOCUS' : self.__LASTFOCUS,
                   '__EVENTTARGET' : self.__EVENTTARGET,
                   '__EVENTARGUMENT' : self.__EVENTARGUMENT,
                   'txtUserName' : self.txtUserName,
                   'btnNext': self.btnNext
                  }

        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.put_pass)

    def put_pass(self,response):

        self.__VIEWSTATEGENERATOR=response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').extract_first()
        self.__EVENTVALIDATION=response.css('input[name="__EVENTVALIDATION"]::attr(value)').extract_first()
        self.__VIEWSTATE=response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()

        self.data={'__VIEWSTATEGENERATOR' : self.__VIEWSTATEGENERATOR,
                   '__EVENTVALIDATION' : self.__EVENTVALIDATION,
                   '__VIEWSTATE' : self.__VIEWSTATE,
                   '__LASTFOCUS' : self.__LASTFOCUS,
                   '__EVENTTARGET' : self.__EVENTTARGET,
                   '__EVENTARGUMENT' : self.__EVENTARGUMENT,
                   'txtPassword' : self.txtPassword,
                   'btnSubmit' : self.btnSubmit
                  }

        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.showFinal)

    def showFinal(self,response):
        att=response.xpath('//*[@id="ctl00_cpStud_lblTotalPercentage"]/b/font').extract_first()
        self.att=float(att[att.index('>')+1:att.index('%')])
        print('\n\n\n\n\n\n YOUR ATTENDANCE IS: ',self.att,'\n\n\n\n\n\n')




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
