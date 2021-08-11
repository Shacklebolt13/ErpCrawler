import scrapy
from scrapy.http.response.html import HtmlResponse
import pandas


class ResCrawler(scrapy.Spider):
    name='ResultCrawler'
    marksSite = 'https://www.gandhionline.in/BEESERP/StudentLogin/Student/OverallMarksSemwise.aspx'
    txtUserName='u'
    txtPassword='p'
    cookie="c"
    __LASTFOCUS=""
    __EVENTTARGET=""
    __EVENTARGUMENT=""
    data :dict
    data={}
    returnJson={}
    semester=1
    end=False
    run=False


    def __init__(self,**kwargs):
        self.txtUserName=kwargs['u']
        self.txtPassword=kwargs['p']
        self.cookie=kwargs['c']
        self.semester=kwargs['s']
        print("GOT TO INIT")
        super(ResCrawler,self).__init__()


    def start_requests(self):
        print(self.txtUserName,self.txtPassword)
        self.cookie=dict(map(lambda x : x.split('='),self.cookie.split(';')))
        print("\nusing cookies:",self.cookie,"\n")
        yield scrapy.FormRequest(method='GET',cookies=self.cookie,url=self.marksSite,callback=self.getThisSemMarks)

    

    def roman(self,semester,increment=True):
        sem=""
        if(semester==9):
            self.end=True
        elif(semester<=3):
            sem+="I"*semester
        elif(semester>3):
            sem=("I"*(5-semester) + "V" + ("I"*(semester-5)))
        if(increment):
            self.semester+=1
        return sem


    def hasThisSemester(self,response:HtmlResponse,sem):
        if(f"{self.roman(sem,increment=False)} SEMESTER" in str(response.body)):
            return True
        else:
            return False


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

   
   
    def getThisSemMarks(self,response: HtmlResponse):
        self.getBasicData(response,reset=True)
        self.data.pop("__EVENTVALIDATION")
        crystalState=response.css('input[name="__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1"]::attr(value)').extract_first()
        self.data.update({f'ctl00$cpStud$btn{self.semester}' : f'{self.roman(self.semester)} SEMESTER','__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1':crystalState})
        self.run=True
        yield scrapy.FormRequest(url=self.marksSite,formdata=self.data,callback=self.getMarks)

   
   
    def getMarks(self,response : HtmlResponse):
        self.returnJson.update({f"{ self.semester -1} semester":self.percentageDetails(response)})
        self.returnJson.update({'totalSems':self.totalSems(response)})
        return self.returnJson


    def totalSems(self,response):
        count=0
        for i in range(1,9):
            if(self.hasThisSemester(response,i)):
                count+=1
        return count




    def handleNaN(self,table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table        

    def percentageDetails(self,response : HtmlResponse):
        table= pandas.read_html("".join(response.xpath(r'//*[@id="ctl00_cpStud_grdSemwise"]').extract()))[0]
        table['FinalGrade']=table['Unnamed: 7']
        table['Credits']=table['Unnamed: 8']
        table['Status']=table['Unnamed: 9']
        table.drop(['Unnamed: 7','Unnamed: 8','Unnamed: 9'],axis=1,inplace=True)
        table=self.handleNaN(table)
        sgpa=response.xpath(r'//*[@id="ctl00_cpStud_lblSemSGPA"]').extract()[0]
        sgpa=(sgpa.split("</font>")[-2]).split(" ")[-1]
        
        cgpa=response.xpath(r'//*[@id="ctl00_cpStud_lblSemCGPA"]').extract()[0]
        cgpa=(cgpa.split("</font>")[-2]).split(" ")[-1]
        return {'CGPA':cgpa,'SGPA':sgpa,'details':table.to_dict()}
