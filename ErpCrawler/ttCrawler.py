import scrapy
from scrapy.http.response.html import HtmlResponse
import pandas


class TTcrawler(scrapy.Spider):
    name='ttCrawler'
    attendanceSite='http://www.gandhionline.in/BEESERP/Login.aspx'
    marksSite = 'https://www.gandhionline.in/BEESERP/StudentLogin/Student/OverallMarksSemwise.aspx'
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
    semester=1
    end=False

    def __init__(self,**kwargs):
        self.txtUserName=kwargs['u']
        self.txtPassword=kwargs['p']
        print("GOT TO INIT")
        super(TTcrawler,self).__init__()


    def start_requests(self):
        print(self.txtUserName,self.txtPassword)
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)



    def parse(self,response : HtmlResponse):
        self.getBasicData(response)
        self.data.update({'txtUserName' : self.txtUserName,'btnNext': self.btnNext })
        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.loginWithPassword)



    def loginWithPassword(self,response : HtmlResponse):
        self.getBasicData(response)
        self.data.update({'txtPassword' : self.txtPassword,'btnSubmit' : self.btnSubmit})
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
        yield self.returnJson #IMPORTANT: to limit crawling to the attendance page
        #yield scrapy.FormRequest(method='GET',url=self.marksSite,callback=self.getMarks)


    def handleNaN(self,table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table



    def attendanceDetails(self,response : HtmlResponse):
        table= pandas.read_html("".join(response.xpath(r'//*[@id="ctl00_cpStud_grdTimetable"]').extract_first()))[0]
        classes= pandas.read_html("".join(response.xpath(r'//*[@id="ctl00_cpStud_grdSubject"]').extract_first()))[0]
        classes=classes.iloc[-1,-3:-1].to_dict()
        
        dicts={}
        l=[]
        for i in list(table.columns)[1:]:
            print(i)
            i=i.split('(')[1][:-1]
            l.append(i)

        dicts['time']=dict(zip(range(len(l)),l)) 
        dicts['subs']=dict(zip(range(len(table.columns)),table.iloc[0][1:]))
        dicts['day']=table.iloc[0][0]

        self.returnJson.update({'schedule':dicts,'classDetails':classes})
        

