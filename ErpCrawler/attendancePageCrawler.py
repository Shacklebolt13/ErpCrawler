import requests
import lxml.html as html
import pandas
from lxml import etree

def attendancePageCrawler(username,password):
    returnJson={'cookie':[]}

    def handleNaN(table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table



    def attendanceDetails(response):
        tree=html.fromstring(response.text)
        table= pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdSubject"]')[0],pretty_print=True))[0]
        att=table.iloc[-1,-1]
        table.drop(table.tail(1).index,inplace=True,axis=0)
        table=handleNaN(table)
        att={'Total':att,'Details':table.to_dict()}
        del table
        table2= pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdDaywise"]')[0],pretty_print=True))[0]
        table2=table2.to_html()
        att['Daywise']=table2.replace("\n","")
        del table2
        del tree
        returnJson.update({'attendance':att})



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
    print('getting login page '+'for  attendance ')

    resp=session.get(url)
    data=getBasicData(resp)
    data.update({'txtUserName' : username,'btnNext': "Next" })
    del resp
    print('putting username: '+ username)
    resp=session.post(url,data)
    if(b"txtUserName" in resp.content):
        print("WRONG USERNAME ",username)
        return([]) #WRONG USERNAME

    del data
    data=getBasicData(resp)
    data.update({'txtPassword' : password,'btnSubmit' : "Submit"})
    print('putting password: ',password)
    resp=session.post(url,data)
    if(b"txtPassword" in resp.content):
        print("WRONG PASSWORD ",password," for ",username)
        return([]) #WRONG PASSWORD

    print("crawling")
    attendanceDetails(resp)
    returnJson['cookie']=session.cookies.get_dict()
    print("crawling complete")

    return returnJson
