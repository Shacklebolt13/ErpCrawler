import requests
import lxml.html as html
import pandas
from lxml import etree
import base64

def dpCrawler(username,password):
    returnJson={}

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

    def dpDetails(resp,session):
        tree=html.fromstring(resp.text)
        att=tree.xpath(r'//*[@id="ctl00_cpStud_lblTotalPercentage"]')[0].text_content()
        returnJson.update({'totalAtt':att})
        tree=tree.xpath(r'//*[@id="ctl00_cpHeader_ucStud_ImgStudPic"]/@src')[0]
        resp=session.get('http://www.gandhionline.in/BEESERP/'+tree)
        returnJson['Dp']=str(base64.b64encode(resp.content),'utf-8')


    url="http://www.gandhionline.in/BEESERP/Login.aspx"
    session=requests.session()
    print('getting login page '+'for  attendance ')

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

    dpDetails(resp, session)


    print("crawling complete")

    return returnJson
