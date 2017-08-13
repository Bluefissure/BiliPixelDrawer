import rsa
import base64
import requests
import urllib.parse
import os

MAIN_HOST = 'http://www.bilibili.com'
API_HOST = 'https://api.bilibili.com'
ACCOUNT_HOST = 'https://account.bilibili.com/api'
BILIAPI_HOST = 'https://api.kaaass.net/biliapi'

"""
BiliPixelDrawer Python Client

:author KAAAsS
"""


# API

def append_param(url, param):
    if url.find('?') == -1:
        return url + '?' + param
    else:
        return url + '&' + param


def get(url, params=None, sign=True):
    """
    调用biliapi进行参数拼接
    :param url:
    :param params:
    :param sign:
    :return:
    """
    if params is None:
        params = {}
    if sign:
        # 调用biliapi
        params['host'] = url
        result = requests.get(BILIAPI_HOST + '/urlgene', params).json()
        result = requests.get(result['url'])
    else:
        # 直接拼接
        param = ''
        for p in params:
            if p != '':
                param = param + p + '=' + str(urllib.parse.quote(str(params[p]))) + '&'
        param = param[:-1]
        result = requests.get(append_param(url, param))
    try:
        return result.json()
    except Exception:
        return result.text


def login(usr, pwd):
    """
    登录B站并获得对应的登录凭据。
    凭据有效期为1个月
    代码来自biliapi_python
    :param usr: 用户名/邮箱/手机号
    :param pwd: 密码
    :return:
    """
    result = {}
    r = get("http://passport.bilibili.com/login?act=getkey", sign=False)
    pwd_hash, key = r['hash'], rsa.PublicKey.load_pkcs1_openssl_pem(r['key'].encode("utf-8"))
    password = str(base64.urlsafe_b64encode(rsa.encrypt((pwd_hash + pwd).encode("utf-8"), key)))[2:-1]
    data = get(ACCOUNT_HOST + "/login/v2", {"userid": usr, "pwd": password})
    if data['code'] != 0:
        return 'Failed to login! Info: ' + data['message']
    result['access_key'] = data['access_key']
    result['expires'] = data['expires']
    return result


def get_cookie(access_key):
    data = get(BILIAPI_HOST + '/user/sso', {'access_key': access_key}, sign=False)
    return data['cookie']


# File Sys

usr_access_key = ''
usr_cookie = ''


def init_account():
    if os.path.exists('user.dat'):
        # 若有则加载
        load_user_data()
    else:
        usr = input("请输入B站账户:\n")
        pwd = input("请输入B站账户密码:\n")
        print("登录中...\n")
        while True:
            try:
                data = login(usr, pwd)
                if isinstance(data, str):
                    print(data)
                    raise Exception()
                else:
                    usr_access_key = data['access_key']
            except Exception as e:
                print("登陆失败，请重试\n")
                usr = input("请输入B站账户:\n")
                pwd = input("请输入B站账户密码:\n")
                continue
            break
        print("登陆成功，正在获取授权信息...\n")
        print(usr_access_key)
        usr_cookie = get_cookie(usr_access_key)
        save_account()


def save_account():
    if os.path.exists('user.dat'):
        return
    f = open('user.dat', 'w')
    f.write(usr_access_key)
    print(usr_access_key)
    f.close()


def load_user_data():
    f = open('user.dat', 'r')
    usr_access_key = f.readline()
    f.close()
    print("已经登录，正在获取授权信息...\n")
    if usr_access_key == '':
        print("登录信息已经过期...\n")
        os.remove('user.dat')
        init_account()
    try:
        usr_cookie = get_cookie(usr_access_key)
    except Exception as e:
        print("登录信息已经过期...\n")
        os.remove('user.dat')
        init_account()

print("BiliPixelDrawer Python Client\n")
init_account()  # 获取cookie，保存在usr_cookie

# TODO 本体功能
