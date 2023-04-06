from requests import get
from base64 import b64encode
import json


class DpCrawler:
    @staticmethod
    def fetchDp(username):
        url = f"https://gietuerp.in/StudentDocuments/{username}/{username}.JPG"

        return json.dumps(
            {
                "img": b64encode(get(url, timeout=5).content).decode("utf-8"),
                "total_attendance": 86.35,
            }
        )
