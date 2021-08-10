import scrapy
from scrapy.http.response.html import HtmlResponse
import pandas


class ErpCrawler(scrapy.Spider):
    name='ErpCrawler'
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
    returnJson={'cookie':[]}
    semester=1
    end=False

    def __init__(self,**kwargs):
        self.txtUserName=kwargs['u']
        self.txtPassword=kwargs['p']
        print("GOT TO INIT")
        super(ErpCrawler,self).__init__()


    def start_requests(self):
        print(self.txtUserName,self.txtPassword)
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)



    def parse(self,response : HtmlResponse):
        self.getBasicData(response)
        a=(response.headers.get('Set-Cookie').decode('utf-8').split(';')[0].split('='))
        self.returnJson['cookie'].append({a[0]:a[1]})
        self.data.update({'txtUserName' : self.txtUserName,'btnNext': self.btnNext })
        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.loginWithPassword)



    def loginWithPassword(self,response : HtmlResponse):
        self.getBasicData(response)
        self.data.update({'txtPassword' : self.txtPassword,'btnSubmit' : self.btnSubmit})
        yield scrapy.FormRequest(url=self.attendanceSite,formdata=self.data,callback=self.gotoSemMarksPage)


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



    def hasThisSemester(self,response:HtmlResponse):
        if(f"{self.roman(self.semester,increment=False)} SEMESTER" in str(response.body)):
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


    def gotoSemMarksPage(self,response : HtmlResponse):
        self.attendanceDetails(response)
        a=response.headers.getlist('Set-Cookie')
        for i in a:
            i=i.decode('utf-8')
            i=i.split(';')[0].split('=')
            i={i[0]:i[1]}
            self.returnJson['cookie'].append(i)
            

        print(response.meta)
        yield self.returnJson #IMPORTANT: to limit crawling to the attendance page
        #yield scrapy.FormRequest(method='GET',url=self.marksSite,callback=self.getMarks)

   
   
    def getThisSemMarks(self,response: HtmlResponse,semester):
        self.getBasicData(response,reset=True)
        self.data.pop("__EVENTVALIDATION")
        crystalState=response.css('input[name="__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1"]::attr(value)').extract_first()
        self.data.update({f'ctl00$cpStud$btn{semester}' : f'{self.roman(semester)} SEMESTER','__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1':crystalState})
        yield scrapy.FormRequest(url=self.marksSite,formdata=self.data,callback=self.getMarks)

   
   
    def getMarks(self,response : HtmlResponse):

        if(self.semester>1):
            self.returnJson.update({f"{self.semester-1} semester":self.percentageDetails(response)})

        if(not self.hasThisSemester(response)):
            
            return self.returnJson
            
        return self.getThisSemMarks(response,self.semester)



    def handleNaN(self,table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table



    def attendanceDetails(self,response : HtmlResponse):
        table= pandas.read_html("".join(response.xpath(r'//*[@id="ctl00_cpStud_grdSubject"]').extract_first()))[0]
        att=table.iloc[-1,-1]
        table.drop(table.tail(1).index,inplace=True,axis=0)
        table=self.handleNaN(table)
        att={'Total':att,'Details':table.to_dict()}
        table2= pandas.read_html("".join(response.xpath(r'//*[@id="ctl00_cpStud_grdDaywise"]').extract_first()))[0]
        table2=table2.to_html()
        att['Daywise']=table2.replace("\n","")
        self.returnJson.update({'attendance':att})
        
        



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
        return {'CGPA':float(cgpa),'SGPA':float(sgpa),'details':table.to_dict()}
