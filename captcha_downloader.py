import os
import requests
import hashlib



def login():
    #Website address to get cookie and captcha
    login_webaddr="http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do"
    #Validator needed to get once
    validator="http://zhjwxk.cic.tsinghua.edu.cn/scripts/validator.jsp"
    #Captcha loading address
    captcha_addr="http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1"
    #Header utilized for login post
    login_headers={'Referer': 'http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept':'text/html, application/xhtml+xml, */*', }
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
    while True:
        s=requests.Session()
        responce = s.get(login_webaddr,headers=headers)
        if responce.url!=login_webaddr:
            s.close()
            continue
        get_check = s.get(validator, headers=headers)
        if get_check.url !=validator:
            s.close()
            continue
        captcha_responce = s.get(captcha_addr, headers=headers)
        if captcha_responce.url !=captcha_addr:
            s.close()
            continue
        #Get and save captcha into file named with the picture md5
        captcha_name=hashlib.md5(captcha_responce.content)
        output_captcha=open(captcha_name.hexdigest()+".jpg","bw")
        output_captcha.write(captcha_responce.content)
        output_captcha.close()
        break
    print(responce.text)

for i in range(256):
    login()
    print(str(i) + " finished")
