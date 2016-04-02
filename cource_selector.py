#Automated Cource Selection (ACS)
#Created by Cheng Xinlun @Tsinghua University, 2015/09/18
#First draft finished debugging @Tsinghua University, 2015/09/20
#Programmed under Python 3.4 with easygui (0.97.4), Pillow (2.9.0), requests (2.7.0)

#Dependencies
#1. Python
#2. easygui, requests, Pillow
#Other dependencies and modules should be commonly-seen and pre-installed in python


#Import necessary modules
import os
import requests
import hashlib
import easygui


#Self-defined class for exception
class XKException(Exception):
    pass


#Class for class selection
class XuanKe():
    
    #Nearly all the web address and post data is defined during class construction
    def __init__(self):
        #Get semester from GUI input
        self.semester=easygui.enterbox(msg="Please enter the semester code (YearBegin-YearEnd-Autumn(1)/Spring(2)/Summer(3))")
        #Get classification of cource from GUI input
        self.class_class=easygui.enterbox(msg="Please enter code for class (rx for non-compulsary, ty for PE)")
        #Get cource number from GUI input
        self.class_number=easygui.enterbox(msg="Please enter cource number")
        #Get cource subnumber from GUI input
        self.class_subnumber=easygui.enterbox(msg="Please enter cource subnumber")
        #Post data to get the token
        self.gettoken_data={"m":self.class_class+"Search", "p_xnxq":self.semester, "tokenPriFlag":self.class_class, "is_zyrxk":"1"}
        #Website address to get cookie and captcha
        self.login_webaddr="http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do"
        #Validator needed to get once
        self.validator="http://zhjwxk.cic.tsinghua.edu.cn/scripts/validator.jsp"
        #Captcha loading address
        self.captcha_addr="http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1"
        #Define post data for login
        self.login_data=""
        #Header utilized for login post
        self.login_headers={'Referer': 'http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept':'text/html, application/xhtml+xml, */*', }
        #Normal post header
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        #Post address for login (HTTPS ensures security)
        self.login_postaddr="https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do"
        #Main cource selection system
        self.xkaddr="http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do"
        #Possible return from site after selection
        self.collision="课程"+self.class_number+"与已选课冲突,不能提交 !"
        self.duplicate="课程号"+self.class_number+"你已经修过此课,重修课请在重修窗口选课,不能提交 !"
        self.alreadyfull="课程"+self.class_number+" "+self.class_subnumber+"课余量已无,不能再选,不能提交 !"
        self.return_dict={self.collision: "Collision with existing cource detected. Exiting...", self.duplicate: "Cource already chose before. Exiting...", self.alreadyfull: "Enrollment reaches maximum. Exiting..."}
        

    #Login and get captcha
    def login(self):
        while True:
            s=requests.Session()
            responce = s.get(self.login_webaddr,headers=self.headers)
            if responce.url!=self.login_webaddr:
                s.close()
                continue
            get_check = s.get(self.validator, headers=self.headers)
            if get_check.url !=self.validator:
                s.close()
                continue
            captcha_responce = s.get(self.captcha_addr, headers=self.headers)
            if captcha_responce.url !=self.captcha_addr:
                s.close()
                continue
            #Get and save captcha into file named with the picture md5
            captcha_name=hashlib.md5(captcha_responce.content)
            output_captcha=open(captcha_name.hexdigest()+".jpg","bw")
            output_captcha.write(captcha_responce.content)
            output_captcha.close()
            #Manual input captcha
            captcha=easygui.enterbox(msg='Please input captcha', image=captcha_name.hexdigest()+".jpg")
            #Login post data construct
            self.login_data = {"j_username":"chengxl14","j_password":"cxl19960610","captchaflag":"login1","_login_image_":captcha}
            #Post login data (verify needed to be turned off in order to connect successfully)
            login_res = s.post(self.login_postaddr, self.login_data, headers=self.login_headers, verify=False)
            if login_res.url!="http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=main":
                s.close()
                continue
            break
        return s
    

    #Get token for the first time from returned webpage
    def gettoken(self, s):
        gettoken_res=s.post(self.xkaddr, self.gettoken_data, headers = self.headers)
        if gettoken_res.url!=self.xkaddr:
            s.close()
            raise XKException("Kicked offline. Relogining...")
        token=gettoken_res.text.split("<input type=\"hidden\" name=\"token\" value=\"",2)[1].split("\"",2)[0]
        return [s, token]


    #Select cource (no search needed which saves a hell lot of time!!)
    def selection(self, s, token):
        selection_data={"m":"save"+str.capitalize(self.class_class)+"Kc", "page":"", "token": token, "p_sort.p1": "", "p_sort.p2": "", "p_sort.asc1": "true", "p_sort.asc2":"true", "p_xnxq": self.semester, "is_zyrxk": "", "tokenPriFlag": self.class_class, "p_kch": self.class_number,"p_kcm": "", "p_kkdwnm": "", "p_kctsm": "", "p_rxklxm": "", "p_rx_id": self.semester+";"+self.class_number+";"+self.class_subnumber+";", "goPageNumber":"1"}
        selection_result=s.post(self.xkaddr, selection_data, headers =self.headers)
        if selection_result.url!=self.xkaddr:
            s.close()
            raise XKException("Kicked offline. Relogining...")
        print(selection_result.text)
        success_or_not=selection_result.text.split("showMsg(\"",2)[1].split("\"",2)[0]
        return success_or_not


    #Main process to be called from outside
    def main_process(self):
        while True:
            #Return a processed session from login() function
            session=self.login()
            try:
                [session, token]=self.gettoken(session)
            except XKException as reason:
                print(str(reason)+"\n")
                continue
            try:
                selection_res=self.selection(session, token)
            except XKException as reason:
                print(str(reason)+"\n")
                continue
            #Process return result from selection
            selection_res_redict=self.return_dict[selection_res]
            print(selection_res_redict+"\n")
            session.close()
            continue
            
        
        
#Create class for cource selection
Myselection=XuanKe()
#Let's do this
Myselection.main_process()


