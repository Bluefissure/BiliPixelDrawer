import rsa
import base64
import requests
import time,json
import urllib.parse
import os
import codecs

MAIN_HOST = 'http://www.bilibili.com'
API_HOST = 'https://api.bilibili.com'
ACCOUNT_HOST = 'https://account.bilibili.com/api'
BILIAPI_HOST = 'https://api.kaaass.net/biliapi'
"""
BiliPixelDrawer Python Client

:author KAAAsS Bluefissure
请在同一目录下建立accountlist.txt文件
每行输入用户名和cookie，以空格分割
cookie格式为
[{'name':***,'value':***,...},
{'name':***,'value':***,...},
......
]
即Chrome中"Edit this cookie"插件导出格式
"""

#下面两个请自行填写
SERVER_HOST = ''
TOKEN = ''

# API

# def append_param(url, param):
#     if url.find('?') == -1:
#         return url + '?' + param
#     else:
#         return url + '&' + param


# def get(url, params=None, sign=True):
#     """
#     调用biliapi进行参数拼接
#     :param url:
#     :param params:
#     :param sign:
#     :return:
#     """
#     if params is None:
#         params = {}
#     if sign:
#         # 调用biliapi
#         params['host'] = url
#         result = requests.get(BILIAPI_HOST + '/urlgene', params).json()
#         result = requests.get(result['url'])
#     else:
#         # 直接拼接
#         param = ''
#         for p in params:
#             if p != '':
#                 param = param + p + '=' + str(urllib.parse.quote(str(params[p]))) + '&'
#         param = param[:-1]
#         result = requests.get(append_param(url, param))
#     try:
#         return result.json()
#     except Exception:
#         return result.text


# def login(usr, pwd):
#     """
#     登录B站并获得对应的登录凭据。
#     凭据有效期为1个月
#     代码来自biliapi_python
#     :param usr: 用户名/邮箱/手机号
#     :param pwd: 密码
#     :return:
#     """
#     result = {}
#     r = get("http://passport.bilibili.com/login?act=getkey", sign=False)
#     pwd_hash, key = r['hash'], rsa.PublicKey.load_pkcs1_openssl_pem(r['key'].encode("utf-8"))
#     password = str(base64.urlsafe_b64encode(rsa.encrypt((pwd_hash + pwd).encode("utf-8"), key)))[2:-1]
#     data = get(ACCOUNT_HOST + "/login/v2", {"userid": usr, "pwd": password})
#     if data['code'] != 0:
#         return 'Failed to login! Info: ' + data['message']
#     result['access_key'] = data['access_key']
#     result['expires'] = data['expires']
#     return result


# def get_cookie(access_key):
#     data = get(BILIAPI_HOST + '/user/sso', {'access_key': access_key}, sign=False)
#     return data['cookie']


class Account:
    def __init__(self,usr,cookie):
        self.usr=usr
        print("%s 成功读取cookie"%(self.usr))
        self.cookies={}
        for item in cookie:
            self.cookies[item['name']]=item['value'] 
    def lefttime(self):
        res = requests.get("http://api.live.bilibili.com/activity/v1/SummerDraw/status",cookies=self.cookies)
        try:
            timeleft=int(res.json()['data']['time'])
            if(timeleft==0):
                self.getpixel()
            else:
                print("Account %s need to wait %s seconds."%(self.usr,timeleft))
        except Exception as e:
            print("Lefttime server error: "+self.usr+str(res.text))
            print(e)
    def drawat(self,x,y,color):
        data = {
            "x_min":x,
            "y_mix":y,
            "x_max":x,
            "y_max":y,
            "color":color
            }
        res = requests.post("http://api.live.bilibili.com/activity/v1/SummerDraw/draw",cookies=self.cookies,data=data)
        try:
            result = res.json()
            if(result['msg']=="success"):
                print("Draw at (%s,%s) color:%s with %s"%(x,y,color,self.usr))
            else:
                print(res.json())
            return True
        except Exception:
            print("Draw server error: "+self.usr+str(res.text))
            return False
    def getpixel(self):
        res = requests.get(SERVER_HOST+'/?token='+TOKEN)
        try:
            pixel = res.json()
            print("Solved %d/%d"%(pixel['total']-pixel['unsolve'],pixel['total']))
            if(self.drawat(pixel['x'],pixel['y'],pixel['color'])):
                callback = requests.get(SERVER_HOST+'/?token='+TOKEN+'&&finx='+str(pixel['x'])+'&&finy='+str(pixel['y']))
                print("Callback "+callback.json()['msg'])
        except Exception as e:
            print(e)
            return res.text





#print("BiliPixelDrawer Python Client\n")
#init_account()  # 获取cookie，保存在usr_cookie

# TODO 本体功能
f=codecs.open("accountlist.txt","r","utf-8")
acclist=[]
for ac in f.readlines():
    ac = ac.split(" ")
    print("成功读取%s账号信息"%(ac[0]))
    acc = Account(ac[0],json.loads(ac[1]))
    acclist.append(acc)
while True:
    for acc in acclist:
        acc.lefttime()
    time.sleep(10)