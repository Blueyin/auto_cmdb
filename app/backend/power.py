# /usr/bin/python2.7
# encoding:utf-8
import requests
import hmac
import base64
from hashlib import sha256
import time
import re
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


names = {}

def get_token():
    payload = {"corpid": "ding31f70bb0d79aa578", "corpsecret": "3Px-shmImbLKgMPawTXi086CRzmuKHKCXM2VkFejs8nLCbOryiK_OWrQ5wtt-Hn4"}
    # print payload
    r = requests.get("https://oapi.dingtalk.com/gettoken", params=payload)
    token_now = json.loads(r.text)["access_token"]
    return token_now


def get_name(access_token, department_id):
    payload = {"access_token": access_token, "department_id": department_id}
    # print payload
    r = requests.get("https://oapi.dingtalk.com/user/simplelist", params=payload)
    return r.text

def get_all_name(access_token, department_id):
    global names
    payload = {"access_token": access_token, "department_id": department_id}
    # print payload
    r = requests.get("https://oapi.dingtalk.com/user/list", params=payload)
    all_name = json.loads(r.text)["userlist"]
    for id in all_name:
        name = id['name']
        emails = id['orgEmail'].split('@')[0]
        names[name] = emails
    return names

def get_listid(access_token, id):
    payload = {"access_token": access_token, "id": id}
    # print payload
    r = requests.get("https://oapi.dingtalk.com/department/list_ids", params=payload)
    list_id = json.loads(r.text)["sub_dept_id_list"]
    return list_id

def get_list(access_token, id):
    payload = {"access_token": access_token, "id": id}
    # print payload
    r = requests.get("https://oapi.dingtalk.com/department/list", params=payload)
    return r.text

def sendmail():
    mail_host = 'smtp.mxhichina.com'
    mail_user = 'chenyin@ishangzu.com'
    mail_passwd = 'Ishangzu123'

    sender = 'chenyin@ishangzu.com'
    receives = 'chenyin@ishangzu.com'

    message = MIMEText('python test', 'plain', 'utf-8')
    message['From'] = Header('chenyin', 'utf-8')
    message['To'] = Header('测试', 'utf-8')

    subject = 'Python 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_passwd)
        smtpObj.sendmail(sender, receives, message.as_string())
        print '邮件发送成功'
    except smtplib.SMTPException:
        print 'Error: 无法发送邮件'

if __name__=='__main__':
    token = get_token()
    # print get_all_name(token)
    list_id = get_listid(token, 52388264)
    # print list_id
    for id in list_id:
        department_id = get_listid(token, id)
        if department_id:
            for ids in department_id:
                get_all_name(token, ids)
        else:
            get_all_name(token, id)

    print json.dumps(names, ensure_ascii=False, encoding='UTF-8')
    print sendmail()

    #    print get_list(token, i)

