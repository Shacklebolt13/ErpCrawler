from requests import post
import pandas as pd


class ExamCrawler:
    @staticmethod
    def fetchAtt(username, sem: int, typ):
        url = "https://gietuerp.in/ExamReport/GetAllScheduledExamForStudents"

        payload = {
            "filterForStudentExamReport[intSemester]": sem,
            "filterForStudentExamReport[vchRollNo]": username,
            "filterForStudentExamReport[intExamTypeID]": typ,
        }

        return post(url, data=payload, timeout=5)

    @staticmethod
    def getExamRes(username, sem, typ):
        response = ExamCrawler.fetchAtt(username, sem, typ)
        data = response.json()["data"]
        return pd.DataFrame.from_records(data).to_html()
