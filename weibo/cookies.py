# -*- coding:utf-8 -*-

import requests
import base64
import json
import re
import rsa
import binascii
import time


def login(username, password):
    login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
    prelogin_url = "https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=MTUwNzgzODE5MjY%3D&rsakt=mod&client=ssologin.js(v1.4.15)&_=1517753790419"
    session = requests.Session()
    resp = session.get(prelogin_url)
    json_data = re.findall(r'(?<=\().*(?=\))', resp.text)[0]
    data = json.loads(json_data)
    # print data
    servertime = data['servertime']
    nonce = data['nonce']
    pubkey = data['pubkey']
    rsakv = data['rsakv']

    username = base64.b64encode(username.encode("utf-8")).decode("utf-8")

    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"), key))

    post_data = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "servertime": servertime,
        "rsakv": rsakv,
        "nonce": nonce,
        "pwencode": "rsa2",
        "sp": sp,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "126",
        "returntype": "TEXT",
    }

    r = session.post(url=login_url, data=post_data)
    # print r.text
    # print r.status_code
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    # print info
    if info["retcode"] == "0":
        # logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        # return json.dumps(cookie)
    else:
        # logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""
        # print(jsonStr)
    Mheaders = {
        "Host": "login.sina.com.cn",
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    # m.weibo.cn 登录的 url 拼接
    _rand = str(time.time())
    mParams = {
        "url": "https://m.weibo.cn/",
        "_rand": _rand,
        "gateway": "1",
        "service": "sinawap",
        "entry": "sinawap",
        "useticket": "1",
        "returntype": "META",
        "sudaref": "",
        "_client_version": "0.6.26",
    }
    murl = "https://login.sina.com.cn/sso/login.php"
    mhtml = session.get(murl, params=mParams, headers=Mheaders)
    mhtml.encoding = mhtml.apparent_encoding
    mpa = r'replace\((.*?)\);'
    mres = re.findall(mpa, mhtml.text)

    # 关键的跳转步骤，这里不出问题，基本就成功了。
    Mheaders["Host"] = "passport.weibo.cn"
    session.get(eval(mres[0]), headers=Mheaders)
    # mlogin = self.session.get(eval(mres[0]), headers=Mheaders)
    # print(mlogin.status_code)
    # 进过几次 页面跳转后，m.weibo.cn 登录成功，下次测试是否登录成功
    Mheaders["Host"] = "m.weibo.cn"
    Set_url = "https://m.weibo.cn"
    pro = session.get(Set_url, headers=Mheaders)
    pa_login = r'isLogin":true,'
    login_res = re.findall(pa_login, pro.text)
    print(login_res)
    cookie1 = session.cookies.get_dict()
    return cookie1

cookies = login('xxxxxx', 'xxxxxx')