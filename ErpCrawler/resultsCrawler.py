import requests
import lxml.html as html
import pandas
from lxml import etree
from requests.cookies import create_cookie

def resultsCrawler(username,password,semester,cookies):

    def handleNaN(table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table



    def semesterResultDetails(response):
        tree=html.fromstring(response.text)
        table= pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdSemwise"]')[0],pretty_print=True))[0]
        #table['FinalGrade']=table['Unnamed: 7']
        #table['Credits']=table['Unnamed: 8']
        #table['Status']=table['Unnamed: 9']
        #table.drop(['Unnamed: 7','Unnamed: 8','Unnamed: 9'],axis=1,inplace=True)
        table=handleNaN(table)
                
        try:
            sgpa=etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_lblSemSGPA"]')[0],pretty_print=True)
            sgpa=(sgpa.split(b"</font>")[-2]).split(b" ")[-1]
        except:
            sgpa=b""

        try:
            cgpa=etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_lblSemCGPA"]')[0],pretty_print=True)
            cgpa=(cgpa.split(b"</font>")[-2]).split(b" ")[-1]
        except:
            cgpa=b""    
        return {'CGPA':str(cgpa,'utf-8'),'SGPA':str(sgpa,'utf-8'),'details':table.to_dict()}
       

    def roman(semester):
        sem=""
        if(semester==9):
            return False
        elif(semester<=3):
            sem+="I"*semester
        elif(semester>3):
            sem=("I"*(5-semester) + "V" + ("I"*(semester-5)))
        return sem

    def getBasicData(response):
            data={}
            print(response.text)
            tree=html.fromstring(response.text)
            __VIEWSTATEGENERATOR=tree.cssselect('input[name="__VIEWSTATEGENERATOR"]')[0].value
            #__EVENTVALIDATION=tree.cssselect('input[name="__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1"]')[0].value
            __VIEWSTATE=tree.cssselect('input[name="__VIEWSTATE"]')[0].value
            data={'__VIEWSTATEGENERATOR' : __VIEWSTATEGENERATOR,
                    #'__CRYSTALSTATEctl00$cpStud$CrystalReportViewer1' : __EVENTVALIDATION,
                    '__VIEWSTATE' : __VIEWSTATE,
                    '__LASTFOCUS' : "",
                    '__EVENTTARGET' : "",
                    '__EVENTARGUMENT' : "",
                    }
            del tree
            return data


    
    urlRes='https://www.gandhionline.in/BEESERP/StudentLogin/Student/OverallMarksSemwise.aspx'
    session=requests.session()
    for k,v in cookies.items():
        session.cookies.set_cookie(requests.cookies.create_cookie(name=k,value=v,domain="www.gandhionline.in"))

    print('getting results page')
    resp=session.get(urlRes)
    data=getBasicData(resp)
    data.update({f'ctl00$cpStud$btn{semester}': f'{roman(semester)} SEMESTER'})
    del resp

    print('getting results for sem',semester)
    resp=session.post(urlRes,data)
    del data

    print("crawling")
    data=semesterResultDetails(resp)
    print("crawling complete")
    return data
