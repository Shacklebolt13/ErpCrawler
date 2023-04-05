from requests import post
import pandas as pd


class AttCrawler:
    @staticmethod
    def fetchAtt(username, sem: int):
        url = "https://gietuerp.in/AttendanceReport/GetAttendanceByRollNo"

        payload = {
            "vvchRollNo": username,
            "vintSemester": sem,
        }

        return post(url, data=payload, timeout=5)

    @staticmethod
    def getAtt(response):
        data = response.json()["dataAttendance"]
        return pd.DataFrame.from_records(data).to_html()
