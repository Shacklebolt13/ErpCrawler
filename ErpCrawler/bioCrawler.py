import requests
import lxml.html as html
import pandas
from lxml import etree

def bioCrawler(username,password,type='dict'):
    returnJson={}

    def handleNaN(table):
            for col in table.columns:
                if(table[col].dtype=="object"):
                    table[col]=table[col].fillna('0')
                else:
                    table[col]=table[col].fillna(0)
            return table


    def bioDetails(response):
        tree=html.fromstring(response.text)#//*[@id="ctl00_cpStud_txtAdmnNo"]
        data={
        'HT. no.' : tree.xpath(r'//*[@id="ctl00_cpStud_txtHTNo"]')[0].value,
        'Registration No.' : tree.xpath(r'//*[@id="ctl00_cpStud_txtAdmnNo"]')[0].value,
        'Roll no.' :tree.xpath(r'//*[@id="ctl00_cpStud_txtRoolNo"]')[0].value,
        'Name' : tree.xpath(r'//*[@id="ctl00_cpStud_txtName"]')[0].value,
        'Program' : tree.xpath(r'//*[@id="ctl00_cpStud_txtProgram"]')[0].value,
        'Branch' : tree.xpath(r'//*[@id="ctl00_cpStud_txtBranch"]')[0].value,
        'Sub-branch' : tree.xpath(r'//*[@id="ctl00_cpStud_txtSubBranch"]')[0].value,
        'Semester' : tree.xpath(r'//*[@id="ctl00_cpStud_txtSem"]')[0].value,
        'Batch' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtBatch"]')[0].value,
        'Joining Year' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtJoinofYear"]')[0].value,
        'Admin Date' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_dtAdminDate_txt"]')[0].value,
        'Lateral' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtLateral"]')[0].value,
        'Autonomous Batch' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtAutoBatch"]')[0].value,
        'Spot Admission' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtSpotAdmission"]')[0].value,
        'Admission Type' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtAdminType"]')[0].value,
        'Admission Category' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtAdminCategory"]')[0].value,
        'Other Admission Type' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtOtherAdmnType"]')[0].value,
        'Caste Category' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtCategory"]')[0].value,
        'Caste Name' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtCasteName"]')[0].value,
        'Fee Reimbursement' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtFeeReimb"]')[0].value,
        'Reimbursement Amt.' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtFeeRemAmt"]')[0].value,
        'Scholarship' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtScholarship"]')[0].value,
        'Education loan' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtEducationLoan"]')[0].value,
        'Date Of Birth' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_dtDateofBirth_txt"]')[0].value,
        'Gender' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_ddGender"]')[0].value,
        'Father\'s Name' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtFatherName"]')[0].value,
        'Father\'s Occupation' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtFatherOccup"]')[0].value,
        'Father\'s Annual Income' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtAnnIncome"]')[0].value,
        'Mother\'s Name' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtMotherName"]')[0].value,
        'Mother\'s Occupation' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtMotherOccup"]')[0].value,
        'Mother\'s Annual Income' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_txtMotherAnnIncome"]')[0].value,
        'Nationality' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_ddNationality"]')[0].value,
        'Bloodgroup' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_ddBloodGroup"]')[0].value,
        'Religion' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_ddReligion"]')[0].value,
        'Mother Tongue' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabAdmissionDet_ddMotherTounge"]')[0].value,
        'Landline' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtLandLine"]')[0].value,
        'Parent\'s Mobile' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtParentMblNo"]')[0].value,
        'Student\'s Mobile' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtStuMblNo"]')[0].value,
        'Parent\'s Email' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtParentEmail"]')[0].value,
        'Student\'s Email' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtStuEmail"]')[0].value,
        'Student\'s Alt. Email' : tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtStuAlterEmail"]')[0].value,
        'Full Correspondence Address': tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtMergeCorAddress"]')[0].value.replace('\r',"").replace('\n',""),
        'Full Permanent Addr': tree.xpath(r'//*[@id="ctl00_cpStud_TabContainerStudMast_TabCommunicationDet_txtMergePerAddress"]')[0].value.replace('\r',"").replace('\n',""),
        }
        
        returnJson.update(data if(type=='dict') else ({'keys':list(data.keys()),'vals':list(data.values())}))
        
         


    def attendanceDetails(response):
        tree=html.fromstring(response.text)
        table= pandas.read_html(etree.tostring(tree.xpath(r'//*[@id="ctl00_cpStud_grdSubject"]')[0],pretty_print=True))[0]
        att=table.iloc[-1,-1]
        table.drop(table.tail(1).index,inplace=True,axis=0)
        table=handleNaN(table)
        att={'Attendance':att}
        del table
        del tree
        returnJson.update(att)



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
    bioUrl="http://www.gandhionline.in/BEESERP/StudentLogin/Student/StudentInformation.aspx"
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
    attendanceDetails(resp)
    
    resp=session.get(bioUrl)
    bioDetails(resp)
    print("crawling complete")

    return returnJson

