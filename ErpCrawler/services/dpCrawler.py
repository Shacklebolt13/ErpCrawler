from requests import get
from base64 import b64encode


class DpCrawler:
    @staticmethod
    def fetchDp(username):
        url = f"https://gietuerp.in/StudentDocuments/{username}/{username}.JPG"

        return b64encode(get(url, timeout=5).content).decode("utf-8")
