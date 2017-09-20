# Automated Cource Selection (ACS)
# Created by Cheng Xinlun @Tsinghua University, 2015/09/18
# First draft finished debugging @Tsinghua University, 2015/09/20

# Dependencies
# 1. Python 3
# 2. requests, Pillow
# 3. scikit-image (skimage)


# Import necessary modules
import time
import warnings
import random

import requests
from tqdm import tqdm

import urls
import ipro
import headers


# Self-defined class for exception
class XKException(Exception):
    pass


# Class for class selection
class XuanKe():
    def __init__(self, sem, cc, cn, cs, user, pswd):
        # Variable initialization
        self.semester = sem
        self.class_class = cc
        self.class_number = cn
        self.class_subnumber = cs
        self.class_count = len(self.class_class)
        self.user = user
        self.pswd = pswd
        self.gettoken_data = [{"m": self.class_class[class_id] + "Search",
                              "p_xnxq": self.semester,
                              "tokenPriFlag": self.class_class[class_id], "is_zyrxk": "1"} for class_id in range(self.class_count)]
        self.login_webaddr = urls.urlCook
        self.validator = urls.urlVali
        self.captcha_addr = urls.urlCapt
        self.login_postaddr = urls.urlLogi
        self.xkaddr = urls.urlCous
        # Generic header
        self.gheader = headers.headGene
        # Login header construction
        self.lheader = headers.headGene
        self.lheader.update(headers.headAcce)
        self.lheader.update(headers.headCook)

    # Login and get captcha
    def login(self):
        while True:
            s = requests.Session()
            responce = s.get(self.login_webaddr, headers=self.gheader)
            if responce.url != self.login_webaddr:
                s.close()
                continue
            get_check = s.get(self.validator, headers=self.gheader)
            if get_check.url != self.validator:
                s.close()
                continue
            captcha_responce = s.get(self.captcha_addr, headers=self.gheader)
            if captcha_responce.url != self.captcha_addr:
                s.close()
                continue
            # Get and save captcha into file named with the picture md5
            output_captcha = open("temp.jpg", "bw")
            output_captcha.write(captcha_responce.content)
            output_captcha.close()
            # Captcha
            captcha = ipro.iip("temp.jpg")
            print(captcha)
            # Login post data construct
            self.login_data = {"j_username": self.user,
                               "j_password": self.pswd,
                               "captchaflag": "login1",
                               "_login_image_": captcha}
            login_res = s.post(self.login_postaddr, self.login_data,
                               headers=self.lheader, verify=False)
            if login_res.url != urls.urlCous + "?m=main":
                s.close()
                continue
            break
        return s

    # Get token for the first time from returned webpage
    def gettoken(self, s, class_id):
        gettoken_res = s.post(self.xkaddr, self.gettoken_data[class_id],
                              headers=self.gheader)
        if gettoken_res.url != self.xkaddr:
            s.close()
            raise XKException("Kicked offline. Relogining...")
        token = gettoken_res.text.split(
              "<input type=\"hidden\" name=\"token\" value=\"", 2)[1].split(
                  "\"", 2)[0]
        return [s, token]

    # Select cource (no search needed which saves a hell lot of time!!)
    def selection(self, s, token, class_id):
        selection_data = {"m": "save" + str.capitalize(self.class_class[class_id]) + "Kc",
                          "page": "", "token": token, "p_sort.p1": "",
                          "p_sort.p2": "", "p_sort.asc1": "true",
                          "p_sort.asc2": "true", "p_xnxq": self.semester,
                          "is_zyrxk": "", "tokenPriFlag": self.class_class[class_id],
                          "p_kch": self.class_number[class_id], "p_kcm": "",
                          "p_kkdwnm": "", "p_kctsm": "", "p_rxklxm": "",
                          "p_rx_id": self.semester + ";" + self.class_number[class_id] +
                          ";" + self.class_subnumber[class_id] + ";", "goPageNumber": "1"}
        selection_result = s.post(self.xkaddr, selection_data,
                                    headers=self.gheader)
        if selection_result.url != self.xkaddr:
            s.close()
            raise XKException("Kicked offline. Relogining...")
        success_or_not = selection_result.text.split("showMsg(\"", 2)[1].split(
            "\"", 2)[0]
        return success_or_not

    # Main process to be called from outside
    def main_process(self):
        while True:
            # Return a processed session from login() function
            session = self.login()
            kick_off = False
            patience = 4
            while True:
                if kick_off or patience == 0:
                    break
                for class_id in range(self.class_count):
                    try:
                        [session, token] = self.gettoken(session, class_id)
                    except XKException as reason:
                        print(str(reason) + "\n")
                        kick_off = True
                        break
                    try:
                        selection_res = self.selection(session, token, class_id)
                        print(selection_res)
                        if selection_res[0:3] == "请输入":
                            patience -= 1
                        else:
                            patience = 4
                        if patience == 0:
                            break
                    except XKException as reason:
                        print(str(reason))
                        continue
                    time.sleep(random.uniform(1.5, 2.5))   
            # Process return result from selection
            # print(selection_res + "\n")
            session.close()
            continue


warnings.simplefilter("ignore")
# Create class for cource selection
sem = "2017-2018-1"
cc = ["rx"] * 1 #class_class, e.g.:rx
cn = ["00780461"] #class_number
cs = ["92"] #class_subnumber
Myselection = XuanKe(sem, cc, cn, cs, "USER", "PASSWORD")
# Let's do this
Myselection.main_process()
