import requests
import encrypt
import time
import random
from bs4 import BeautifulSoup


def get_timestamp():
    """获取当前时间戳"""
    return int(round(time.time() * 1000))


def get_login_info(session: requests.Session = None):
    """获取aeskey和excution

    Args:
        session (requests.Session, optional): Session对象. Defaults to None.

    Returns:
        str: aeskey和excution
    """
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://ids.ctgu.edu.cn/authserver/login",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://ids.ctgu.edu.cn/authserver/login"
    response = session.get(url, headers=headers)
    mysoup = BeautifulSoup(response.text, 'html.parser')
    aeskey = mysoup.find(
        'input', attrs={'id': 'pwdEncryptSalt'}).attrs['value']
    excution = mysoup.find('input', attrs={'id': 'execution'}).attrs['value']
    return aeskey, excution


def get_token(session: requests.Session):
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ids.ctgu.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.ctgu.edu.cn%2Fjwapp%2Fsys%2Femaphome%2Fportal%2Findex.do%3FforceCas%3D1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://ids.ctgu.edu.cn/authserver/qrCode/getToken"
    params = {
        "ts": get_timestamp()
    }
    response = session.get(url, headers=headers, params=params, verify=False)


def login(user: dict, session: requests.Session, aeskey, excution):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://ids.ctgu.edu.cn",
        "Referer": "http://ids.ctgu.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.ctgu.edu.cn%2Fjwapp%2Fsys%2Femaphome%2Fportal%2Findex.do%3FforceCas%3D1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    url = "http://ids.ctgu.edu.cn/authserver/login"
    params = {
        "service": "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do?forceCas=1"
    }
    data = {
        "username": user.get("username"),
        "password": encrypt.encrypt_password(user.get('password'), aeskey),
        "captcha": "",
        "_eventId": "submit",
        "cllt": "userNameLogin",
        "dllt": "generalLogin",
        "lt": "",
        "execution": excution
    }
    session.headers.update(headers)
    response = session.post(url, data=data, params=params)
    if response.status_code == 200:
        print('登录成功')
    else:
        print('登录失败,请检查账号密码是否正确')


def get_token(session: requests.Session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "http://ids.ctgu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    url = "http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do"
    params = {
        "forceCas": "1",
        "ticket": "ST-711282-VPV8SevPpnYwLK8KfWfXzdQb44Ulocalhost"
    }
    session.get(url, headers=headers, params=params, verify=False)


def get_grade_token(session: requests.Session):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "$Cookie": "GS_SESSIONID=71aa0730ff9c07970ba05a2d7c7e8bed; EMAP_LANG=zh; _WEU=X*PDxy_T31s4iKL5da5NYRSv*4H0Q*bO7s4J78GfjAin9XTWnIs5OqwOr4uFQRKXyG2VRMGKC75LBp41jBNqCfOy8zRM690_ODT53BT6275lYkqtdDQW6SgrFRn7XjWdr9uyJoPsUS4zFe4bYtbsyQ9QlgHMw250vKUDtVYmbKRMYY1_Yo0jSnnSOvH5Ikxy5ZoLp1v7QTwe5OZ3jEEpH6YzfsIUveUP5daNf*fJpfesLwTW2JMTVUMQqJ9t*8N385n5ILZUtw8I89BUntRYeo..; JSESSIONID=ARRawgDPwNHy5umTBc_boKmpo-MSoJ_-iha5tpRersGD7Up4FSgt\\u0021-1611273288",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    url = "http://jwxt.ctgu.edu.cn/jwapp/sys/funauthapp/api/getAppConfig/cjcx-4768574631264620.do"
    params = {
        "v": str(random.randint(1, 10**17 - 1)).zfill(17)
    }
    response = session.get(url, headers=headers, params=params, verify=False)


def get_grade(session: requests.Session):
    grade_dict = {}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://jwxt.ctgu.edu.cn",
        "Referer": "http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
    data = {
        "querySetting": "[{\"name\":\"SFYX\",\"caption\":\"是否有效\",\"linkOpt\":\"AND\",\"builderList\":\"cbl_m_List\",\"builder\":\"m_value_equal\",\"value\":\"1\",\"value_display\":\"是\"},{\"name\":\"SHOWMAXCJ\",\"caption\":\"显示最高成绩\",\"linkOpt\":\"AND\",\"builderList\":\"cbl_m_List\",\"builder\":\"m_value_equal\",\"value\":\"0\",\"value_display\":\"否\"}]",
        "*order": "-XNXQDM,-KCH,-KXH",
        "pageSize": "10",
        "pageNumber": "1"
    }
    response = session.post(url, headers=headers, data=data, verify=False)
    totalSize = response.json()["datas"]["xscjcx"]["totalSize"]
    pageNumber = int(response.json()["datas"]["xscjcx"]["pageNumber"])
    pageSize = int(data["pageSize"])
    while pageNumber < totalSize / pageSize + 1:
        data["pageNumber"] = str(pageNumber)
        response = session.post(url, headers=headers, data=data, verify=False)
        pageNumber = int(response.json()["datas"]["xscjcx"]["pageNumber"]) + 1
        for index in range(len(response.json()["datas"]["xscjcx"]["rows"])):
            lesson_name = response.json()["datas"]["xscjcx"]["rows"][index]["XSKCM"]
            lesson_grade = response.json()["datas"]["xscjcx"]["rows"][index]["ZCJ"]
            grade_dict[lesson_name] = lesson_grade
    return grade_dict
        


if __name__ == '__main__':
    user={
        "username": "xxxxxxxxxxx",
        "password": "xxxxxxxxxxx",
    }
    session = requests.Session()
    aeskey, excution = get_login_info(session)
    get_token(session)
    login(user, session, aeskey, excution)
    get_token(session)
    get_grade_token(session)
    grade_dict = get_grade(session)
    print(grade_dict)