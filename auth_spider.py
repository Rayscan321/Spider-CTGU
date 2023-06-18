import requests
import time
from lxml import etree
import execjs
import ddddocr

class CTGU: 
    def __init__(self, username, password) -> None:
        self.__username = username
        self.__password = password
        self.__session = requests.Session()
        self.__excution = None
        self.__pwdEncryptSalt = None
        self.ticket = self.__login()

    def __get_encrypt_info(self):
        """
        Gets the encryption information needed to login to the CTGU student portal.
        
        :return: None
        """
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }
        url = "http://ids.ctgu.edu.cn/authserver/login"
        params = {
            "service": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1"
        }
        response = self.__session.get(url, headers=headers, params=params, verify=False)
        html = etree.HTML(response.text)
        self.__pwdEncryptSalt = html.xpath('//*[@id="pwdEncryptSalt"]/@value')[0]
        self.__excution = html.xpath('//*[@id="execution"]/@value')[0]

    def __get_encrypted_password(self):
        with open('E:/python_program/spider/spider_ctgu/auth/pwd.js', 'r') as f:
            jscode = f.read()
            ctx = execjs.compile(jscode)
            encrypted_password = ctx.call('encryptPassword', self.__password, self.__pwdEncryptSalt)
            return encrypted_password
        
    def __if_need_captcha(self):
        """
        Checks if captcha is needed for authentication.

        :return: A boolean value indicating if captcha is needed.
        """
        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://ids.ctgu.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.ctgu.edu.cn%2Fjwapp%2Fsys%2Femaphome%2Fportal%2Findex.do%3FforceCas%3D1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        "X-Requested-With": "XMLHttpRequest"
        }
        url = "http://ids.ctgu.edu.cn/authserver/checkNeedCaptcha.htl"
        params = {
            "username": self.__username,
            "_":str(int(time.time()*1000))
        }
        response = self.__session.get(url, headers=headers, params=params, verify=False)
        return response.json()['isNeed']
        
    def __get_captcha(self):
        """
        This function retrieves a captcha image from the website and uses DdddOcr to 
        classify the characters in the image. 

        :return: A string representing the characters in the captcha image.
        """
        headers = {
        "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://ids.ctgu.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.ctgu.edu.cn%2Fjwapp%2Fsys%2Femaphome%2Fportal%2Findex.do%3FforceCas%3D1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }
        url = "http://ids.ctgu.edu.cn/authserver/getCaptcha.htl"
        params = {
            str(int(time.time()*1000)): ""
        }
        response = self.__session.get(url, headers=headers, params=params, verify=False)
        with open('./captcha.png', 'wb') as f:
            f.write(response.content)
        ocr = ddddocr.DdddOcr()
        with open('./captcha.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res

    def __login(self):
        """
        Private method that logs into a website using credentials and session information.
        __get_encrypt_info, __if_need_captcha and __get_captcha are called to ensure a smooth login process.
        Sends a post request to the website with the necessary login parameters.
        Returns nothing, but prints response headers.
        """
        self.__get_encrypt_info()
        if(self.__if_need_captcha() == 'false'):
            self.__get_captcha()
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://ids.ctgu.edu.cn",
        "Pragma": "no-cache",
        "Referer": "http://ids.ctgu.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.ctgu.edu.cn%2Fjwapp%2Fsys%2Femaphome%2Fportal%2Findex.do%3FforceCas%3D1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }
        url = "http://ids.ctgu.edu.cn/authserver/login"
        params = {
            "service": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1"
        }
        data = {
            "username": self.__username,
            "password": self.__get_encrypted_password(),
            "captcha": "",
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "dllt": "generalLogin",
            "lt": "",
            "execution": self.__excution,
        }
        response = self.__session.post(url, headers=headers, params=params, data=data, verify=False, allow_redirects=False)
        return response.headers['location'].split('=')[-1]

    def __get_need_cookies(self):
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ids.ctgu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do"
        params = {
            "forceCas": "1",
            "ticket": self.ticket
        }
        self.__session.get(url, headers=headers, params=params, verify=False, allow_redirects=False)
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ids.ctgu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do"
        params = {
            "forceCas": "1"
        }
        self.__session.get(url, headers=headers, params=params, verify=False)
        headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
        "X-Requested-With": "XMLHttpRequest"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/i18n.do"
        params = {
            "appName": "emaphome",
            "EMAP_LANG": "zh"
        }
        self.__session.get(url, headers=headers, params=params, verify=False)
        headers = {
        "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/main.do"
        response = self.__session.get(url, headers=headers)
        headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://jwxt.ctgu.edu.cn",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
        "X-Requested-With": "XMLHttpRequest"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/appShow.do"
        data = {
            "id": "70502b06201545cda7048845d8075783"
        }
        response = self.__session.post(url, headers=headers, data=data, verify=False)

    def __get_one_page_grade(self, page=1, page_size=10):
        grades = {}
        self.__get_need_cookies()
        self.__session.cookies.set('_ht', 'person')
        self.__session.cookies.set('EMAP_LANG', 'zh')
        self.__session.cookies.set('CASTGC', None)
        self.__session.cookies.set('happyVoyagePersonal', None)
        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://jwxt.ctgu.edu.cn",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        "X-Requested-With": "XMLHttpRequest"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
        data = {
            "querySetting": "[{\"name\":\"SFYX\",\"caption\":\"是否有效\",\"linkOpt\":\"AND\",\"builderList\":\"cbl_m_List\",\"builder\":\"m_value_equal\",\"value\":\"1\",\"value_display\":\"是\"},{\"name\":\"SHOWMAXCJ\",\"caption\":\"显示最高成绩\",\"linkOpt\":\"AND\",\"builderList\":\"cbl_m_List\",\"builder\":\"m_value_equal\",\"value\":\"0\",\"value_display\":\"否\"}]",
            "*order": "-XNXQDM,-KCH,-KXH",
            "pageSize": str(page_size),
            "pageNumber": str(page),
        }
        response = self.__session.post(url, headers=headers, data=data, verify=False).json()
        total_grades = response["datas"]["xscjcx"]["totalSize"]
        for i in response["datas"]["xscjcx"]["rows"]:            
            grades[i["KCM"]] = i["XSZCJMC"]
        return total_grades, grades

    def get_grades(self):
        grades = {}
        total_grades, grades = self.__get_one_page_grade()
        if(total_grades//10 == 0):
            total_pages = total_grades//10
        else:
            total_pages = total_grades//10 + 1
        for i in range(2, total_pages+1):
            page_size = 10
            if(i == total_pages):
                page_size = total_grades%10
            total_grades, grades_page = self.__get_one_page_grade(page=i, page_size=page_size)
            total_pages = total_pages - 1
            grades.update(grades_page)
        return grades

    def get_user_info(self):
        self.__get_need_cookies()
        info = {}
        headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "http://jwxt.ctgu.edu.cn",
        "Pragma": "no-cache",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
        "X-Requested-With": "XMLHttpRequest"
        }
        url = "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/getLoginUser.do"
        response = self.__session.post(url, headers=headers, verify=False)
        info['学号'] = response.json()['datas']['ACCOUNTID']
        info['姓名'] = response.json()['datas']['ACCOUNTNAME']
        info['邮箱'] = response.json()['datas']['EMAIL']
        info['手机号'] = response.json()['datas']['CELLPHONE']
        return info

if __name__ == "__main__":
    user = CTGU('username', 'password')
    print(user.get_grades())
    print(user.get_user_info())
    