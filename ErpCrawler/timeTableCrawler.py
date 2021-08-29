import requests
import lxml.html as html
import pandas
from lxml import etree

def timeTableCrawler(username,password):
    returnJson={}

    def handleNaN(table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table



    def timeTableDetails(response):
        tree=html.fromstring(response.text)
        dicts={}
        try:
            table= pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdTimetable"]')[0],pretty_print=True))[0]
            l=[]
            for i in list(table.columns)[1:]:
                print(i)
                i=i.split('(')[1][:-1]
                l.append(i)
            
            dicts['time']=dict(zip(range(len(l)),l)) 
            dicts['subs']=dict(zip(range(len(table.columns)),table.iloc[0][1:]))
            dicts['day']=table.iloc[0][0]
            del table
        except:
            pass     
        classes=pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdSubject"]')[0],pretty_print=True))[0]
        classes=classes.iloc[-1,-3:-1].to_dict()

        returnJson.update({'schedule':dicts,'classDetails':classes})
        del dicts
        del classes
       


    def getBasicData(response):
            data={}
            tree=html.fromstring(response.text)
            __VIEWSTATEGENERATOR=tree.cssselect('input[name="__VIEWSTATEGENERATOR"]')[0].value
            __EVENTVALIDATION=tree.cssselect('input[name="__EVENTVALIDATION"]')[0].value
            __VIEWSTATE=tree.cssselect('input[name="__VIEWSTATE"]')[0].value
            data={'__VIEWSTATEGENERATOR' : __VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION' : __EVENTVALIDATION,
                    '__VIEWSTATE' : __VIEWSTATE,
                    '__LASTFOCUS' : "",
                    '__EVENTTARGET' : "",
                    '__EVENTARGUMENT' : "",
                    }
            del tree
            return data


    url="http://www.gandhionline.in/BEESERP/Login.aspx"
    session=requests.session()
    print('getting login page for time table')

    resp=session.get(url)
    data=getBasicData(resp)
    data.update({'txtUserName' : username,'btnNext': "Next" })
    del resp
    print('putting username: '+ username)
    resp=session.post(url,data)
    
    del data
    data=getBasicData(resp)
    data.update({'txtPassword' : password,'btnSubmit' : "Submit"})
    print('putting password: ',password)
    resp=session.post(url,data)
    
    print("crawling")
    timeTableDetails(resp)
    print("crawling complete")
    return returnJson