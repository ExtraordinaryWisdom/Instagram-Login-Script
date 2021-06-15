from datetime import datetime
import requests
import re
import pickle


class Token:

    def __init__(self, URL):
        self.url = URL

    def __call__(self, *args, **kwargs):
        return self.url(*args, **kwargs)

class Form:

    def __init__(self, User, Pass):
        self.User = User
        self.Pass = Pass

    @Token
    def cookie(url="https://www.instagram.com/"):
        req = dict(requests.get(f'{url}', headers={"User-Agent": "Mozilla/5.0 (X11; Linux armv8l; rv:78.0) Gecko/20100101 Firefox/78.0"}).cookies)
        return req

    @property
    def data(self):
        return (
            dict(
                    {
                        'username': self.User,
                        'enc_password': "#PWD_INSTAGRAM_BROWSER:0:%s:%s" %(int(datetime.now().timestamp()), self.Pass),
                    }, 
                    **pickle.loads(
                        b'\x80\x03}q\x00(X\x0b\x00\x00\x00queryParamsq\x01X\x02\x00\x00\x00{}q\x02X\r\x00\x00\x00optIntoOneTapq\x03X\x05\x00\x00\x00falseq\x04X\x11\x00\x00\x00stopDeletionNonceq\x05X\x00\x00\x00\x00q\x06X\x14\x00\x00\x00trustedDeviceRecordsq\x07h\x02u.'      
                    )
                )
            )

    def __len__(self):
        return len(repr(self.data))

    def header(self):
        return b'\x80\x03}q\x00(X\x04\x00\x00\x00Hostq\x01X\x11\x00\x00\x00www.instagram.comq\x02X\n\x00\x00\x00User-Agentq\x03XD\x00\x00\x00Mozilla/5.0 (X11; Linux armv8l; rv:78.0) Gecko/20100101 Firefox/78.0q\x04X\x06\x00\x00\x00Acceptq\x05X\x03\x00\x00\x00*/*q\x06X\x0f\x00\x00\x00Accept-Languageq\x07X\x0e\x00\x00\x00en-US,en;q=0.5q\x08X\x0f\x00\x00\x00Accept-Encodingq\tX\x11\x00\x00\x00gzip, deflate, brq\nX\x0c\x00\x00\x00Content-Typeq\x0bX!\x00\x00\x00application/x-www-form-urlencodedq\x0cX\x10\x00\x00\x00X-Requested-Withq\rX\x0e\x00\x00\x00XMLHttpRequestq\x0eX\x06\x00\x00\x00Originq\x0fX\x19\x00\x00\x00https://www.instagram.comq\x10X\x03\x00\x00\x00DNTq\x11X\x01\x00\x00\x001q\x12X\n\x00\x00\x00Connectionq\x13X\n\x00\x00\x00keep-aliveq\x14X\x07\x00\x00\x00Refererq\x15X\x1a\x00\x00\x00https://www.instagram.com/q\x16u.'

    @property
    def items(self):
        cc = self.cookie()
        return (cc['csrftoken'], re.sub("': '", "=", str(cc)[2:-2]).replace("', '", "; "))

class post(Form):

    def __init__(self, User, Pass):
        super(post, self).__init__(User, Pass)
        self.user = User
        self.Pass = Pass

    def headers(self):
        item = self.items
        return (dict({
            "X-CSRFToken" : item[0],
            "Content-Length": f"{self.__len__()}",
            "Cookie": item[1]
            },
            **pickle.loads(self.header())
        ))

    @property   
    def login(self):
        req = requests.post("https://www.instagram.com/accounts/login/ajax/",
                headers=self.headers(), data=self.data)            
        return (
            {
                'auth': req.json().get('authenticated'),
                'cookies': dict(req.cookies)
            }
        )
        
    def check_auth(self):
        log = self.login
        if log.get('auth')  == True:
            with open("cookies.txt", "w") as ck:
                ck.write(str(log.get("cookies")))
            return "Logged in Successfully"
        else:
            return "Incorrect password"
