import requests
class CTGU:
    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password

    '''
    获取最近两个学期的成绩
    返回两个列表，分别为科目和成绩
    return:
        Subject[]
        Core[]
    '''
    def GetRecentGrades(self):
        '''
        param str userName  用户名
        param str passWord   密码
        param int pageNum   成绩页页数
        '''
        Subject = []
        Core = []
        login_pageUrl = 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/index.do'
        login_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/doDbLogin.do'
        userInfo_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/getLoginUser.do'
        homePage_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do'
        gradesLog_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/funauthapp/api/getAppConfig/cjcx-4768574631264620.do'
        grades_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'Origin': 'http://jwxt.ctgu.edu.cn',
            'Referer': 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/index.do',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'jwxt.ctgu.edu.cn',
        }

        data_login = {
            'userId': self.Username,
            'password': self.Password,
            'vcode': '',
        }

        data_getGrades = {
            'querySetting': '[{"name":"XNXQDM","value":"2022-2023-1,2022-2023-2","linkOpt":"and","builder":"m_value_equal"},{"name":"SFYX","caption":"是否有效","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"1","value_display":"是"},{"name":"SHOWMAXCJ","caption":"显示最高成绩","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"0","value_display":"否"}]',
            '*order': '-XNXQDM,-KCH,-KXH',
            'pageSize': '10',
            'pageNumber': '1',
        }
        
        #构建session对话
        session = requests.Session()
        session.headers.update(headers)
        #访问登录页面
        session.get(url=login_pageUrl)
        #模拟登录
        try:
            session.post(url=login_url, data=data_login)
        except Exception:
            return '您的账号或密码错误，请仔细检查'
        #获取登陆者信息
        # userInfo = session.post(url=userInfo_url).json()
        # print(userInfo['datas']['ACCOUNTNAME'])
        #获取个人信息网首页
        session.get(url=homePage_url)
        print('成功获取个人首页')
        #请求获取个人成绩
        #更新headers
        session.headers.update({'Referer':'http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh'})
        session.get(url=gradesLog_url)
        grades_json = session.post(url=grades_url, data=data_getGrades).json()
        for index in range(0,grades_json['datas']['xscjcx']['totalSize']):
            if index > 9:
                index = 0
                pageNum = 1
                data_getGrades['pageNumber'] = str(pageNum+1)
                grades_json = session.post(url=grades_url, data=data_getGrades).json()
            Subject.append(grades_json['datas']['xscjcx']['rows'][index]['XSKCM'])
            Core.append(grades_json['datas']['xscjcx']['rows'][index]['XSZCJMC'])
        return Subject, Core

    '''
    获取全部的成绩
    返回两个列表，分别为科目和成绩
    return:
        Subject[]
        Core[]
    '''
    def GetAllGrades(self):
        '''
        param str SubjectName 科目名称
        '''
        '''
        param str userName  用户名
        param str passWord   密码
        param int pageNum   成绩页页数
        '''
        pageNum = 1
        i = 0
        Subject = []
        Core = []
        login_pageUrl = 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/index.do'
        login_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/doDbLogin.do'
        userInfo_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/getLoginUser.do'
        homePage_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/emaphome/portal/index.do'
        gradesLog_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/funauthapp/api/getAppConfig/cjcx-4768574631264620.do'
        grades_url = 'http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'Origin': 'http://jwxt.ctgu.edu.cn',
            'Referer': 'http://jwxt.ctgu.edu.cn/jwapp/sys/yjsrzfwapp/dbLogin/index.do',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'jwxt.ctgu.edu.cn',
        }

        data_login = {
            'userId': self.Username,
            'password': self.Password,
            'vcode': '',
        }

        data_getGrades = {
            'querySetting': '[{"name":"SFYX","caption":"是否有效","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"1","value_display":"是"},{"name":"SHOWMAXCJ","caption":"显示最高成绩","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"0","value_display":"否"}]',
            '*order': '-XNXQDM,-KCH,-KXH',
            'pageSize': '10',
            'pageNumber': '1',
        }
        
        #构建session对话
        session = requests.Session()
        session.headers.update(headers)
        #访问登录页面
        session.get(url=login_pageUrl)
        #模拟登录
        try:
            session.post(url=login_url, data=data_login)
        except Exception:
            return '您的账号或密码错误，请仔细检查'
        #获取登陆者信息
        # userInfo = session.post(url=userInfo_url).json()
        # print(userInfo['datas']['ACCOUNTNAME'])
        #获取个人信息网首页
        session.get(url=homePage_url)
        print('成功获取个人首页')
        #请求获取个人成绩
        #更新headers
        session.headers.update({'Referer':'http://jwxt.ctgu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh'})
        session.get(url=gradesLog_url)
        grades_json = session.post(url=grades_url, data=data_getGrades).json()
        for index in range(0,grades_json['datas']['xscjcx']['totalSize']):
            if i > 9:
                i = 0
                pageNum += 1
                data_getGrades['pageNumber'] = str(pageNum)
                grades_json = session.post(url=grades_url, data=data_getGrades).json()
            Subject.append(grades_json['datas']['xscjcx']['rows'][i]['XSKCM'])
            Core.append(grades_json['datas']['xscjcx']['rows'][i]['XSZCJMC'])
            i += 1
        return Subject, Core

    '''
    查询指定科目成绩
    param str Specify 想查询的科目名称
    '''
    def SearchCore(self, Specify):
        Subject, Core = CTGU.GetAllGrades(self=self)
        dict = {}
        for i in range(0, len(Subject)):
             dict.update({Subject[i]:Core[i]})
        return dict[Specify]
        

if __name__ == '__main__':
    
