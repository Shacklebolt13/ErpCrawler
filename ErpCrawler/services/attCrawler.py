from requests import post
import pandas as pd
from fractions import Fraction
import json


def replace_fraction(val):
    try:
        return float(val)
    except ValueError:
        return float(Fraction(val.replace(" ", "")))


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
    def getAtt(username, sem):
        print(username, sem)
        response = AttCrawler.fetchAtt(username, sem)
        data = response.json()["dataAttendance"]
        df = pd.DataFrame.from_records(data)
        data = {"summary": df.copy().to_html()}
        df.drop("AttendanceDate", axis=1, inplace=True)
        # replace all 0/0 with 0
        df = df.replace("0/0", "0")
        # replace all number/number with evaluated fraction
        df = df.applymap(replace_fraction)

        data["subwise"] = df.sum().to_dict()
        return json.dumps(data)


if __name__ == "__main__":
    print(AttCrawler.getAtt("20CSE232", -1))
