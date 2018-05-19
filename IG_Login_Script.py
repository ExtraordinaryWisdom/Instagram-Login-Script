import requests

BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
USERNAME = '******'
PASSWD = '*****'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
 Chrome/59.0.3071.115 Safari/537.36'

session = requests.Session()
session.headers = {'user-agent': USER_AGENT}
session.headers.update({'Referer': BASE_URL})


req = session.get(BASE_URL)

session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
login_data = {'username': USERNAME, 'password': PASSWD}
login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})

cookies = login.cookies

print(login.text)

check = '"authenticated": true'

current_result = login.text

if check in current_result:
    print("correct")
else:
    print("wrong")



