#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import json
import os
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from MOAS.settings import BASE_DIR
from applications.process.models import ProcessModel
from applications.user.models import UserModel


def load_conf():
    file = open(os.path.join(BASE_DIR, 'conf', 'conf.json'))
    conf = file.read()
    file.close()
    return json.loads(conf)


def send_mail():
    conf = load_conf()
    from_addr = conf.get('system-email')
    password = conf.get('system-email-pwd')
    if ':' not in conf.get('email-address'):
        smtp_server, smtp_port = conf.get('email-address'), 80
    else:
        smtp_server, smtp_port = conf.get('email-address').split(':')
    obj = ProcessModel.objects.all().order_by('-create_time').first()
    if not obj.at_leader: return
    server = smtplib.SMTP_SSL()
    try:
        server.connect(smtp_server, smtp_port)
        server.login(from_addr, password)
        for i in re.findall(r'"(\d)"', obj.at_leader):
            user = UserModel.objects.filter(id__exact=i)
            if not user: continue
            to_addr = user.first().email
            msg = MIMEText(f'新收到一条来自 【{obj.organizer.get_full_name()}】 发出的 【{obj.title}】 流程申请，等待您审批。\n\n{obj.demand}', 'plain', 'utf-8')
            msg['From'] = Header(from_addr)
            msg['To'] = Header(to_addr)
            msg['Subject'] = Header('流程审批提醒邮件')
            server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()
