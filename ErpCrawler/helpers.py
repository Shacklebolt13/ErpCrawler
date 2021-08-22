import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ErpCrawler.settings as settings
import threading
from django.core.mail import EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        print('sending mail to',self.recipient_list)
        msg.send()
        print('sent')


def encryptResp(password,otp):
    
    #salt = os.urandom(16)
    # kdf = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    #     length=32,
    #     salt=salt,
    #     iterations=100000,
    # )
    # password=kdf.derive(password)
    #key = base64.urlsafe_b64encode(password)
    fernet=Fernet(password)
    return fernet.encrypt(otp.encode())