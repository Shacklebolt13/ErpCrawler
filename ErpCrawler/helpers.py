import base64
import random, string
import ErpCrawler.settings as settings
import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject, self.html_content, "GIETU OFFICIAL", self.recipient_list
        )
        msg.content_subtype = "html"
        print("sending mail to", self.recipient_list)
        msg.send()
        print("sent")


def encryptResp(data, fuzzLen, dummy=False, dummyLen=6, onlyDigit=False):
    if dummy:
        fuzzTot = fuzzLen * 2 + dummyLen
    else:
        fuzzTOt = fuzzLen * 2
    choices = (
        (string.ascii_letters + string.digits) if (not onlyDigit) else string.digits
    )
    extra = "".join(random.choices(choices, k=fuzzTot))
    data = extra[:fuzzLen] + data + extra[fuzzLen : fuzzLen * 2]
    data = base64.b64encode(data.encode())
    data = str(data, "utf-8")
    data = data.swapcase()[::-1]
    if dummy:
        return (data, extra[fuzzLen * 2 :])
    else:
        return data
