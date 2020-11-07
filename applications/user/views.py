#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import json
import os
import time

import schedule
from django.conf import settings

from MOAS.settings import BASE_DIR


def jwt_get_user_secret(user):
    return user.user_secret


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': 'M&OAS ' + token,
        'identity': user.id,
        'username': user.username,
        'fullname': user.get_full_name(),
    }


def __public():
    from Crypto.PublicKey import RSA
    rsa = RSA.generate(1024)
    private_pem = str(rsa.exportKey(), encoding='utf-8')
    with open(os.path.join(settings.BASE_DIR, 'applications', 'user', 'private.pem'), 'w') as f:
        f.write(private_pem)
        f.close()
    public_pem = str(rsa.publickey().exportKey(), encoding='utf-8')
    with open(os.path.join(settings.BASE_DIR, 'applications', 'user', 'public.pem'), 'w') as f:
        f.write(public_pem)
        f.close()


def public():
    import _thread
    schedule.every().monday.at('05:00').to(__public)

    def _():
        while 1:
            schedule.run_pending()
            time.sleep(5)

    if not os.path.isfile(
            os.path.join(settings.BASE_DIR, 'applications', 'user', 'private.pem')
    ) or not os.path.isfile(
        os.path.join(settings.BASE_DIR, 'applications', 'user', 'public.pem')
    ): _thread.start_new_thread(__public, ())

    _thread.start_new_thread(_, ())


def workplace(f=False):
    file = open(os.path.join(BASE_DIR, 'applications', 'user', 'workplace.json'), 'r', encoding='UTF-8')
    info = json.loads(file.read())
    file.close()
    if f: return info
    result = list()
    for i in info.values():
        i['children'] = list(i.get('children').values())
        result.append(i)
    return result


def navs(_):
    return [
        {
            'title': 'Dashboard',
            'href': 'menu/dashboard/dashboard.html',
            'fontFamily': 'ok-icon',
            'icon': '&#xe61b;',
            'spread': True,
            'isCheck': True,
            'display': True
        },
        {
            'title': '流程处理',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe6d7;',
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '我提交的流程',
                    'href': 'menu/process/submitProcess.html',
                    'spread': False
                },
                {
                    'display': True,
                    'title': '我处理的流程',
                    'href': 'menu/process/handleProcess.html',
                    'spread': False
                }
            ]
        },
        {
            'title': '考勤处理',
            'fontFamily': 'ok-icon',
            'icon': '&#xe640;',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '个人考勤',
                    'href': 'menu/attendance/attendance.html',
                    'spread': False
                }
            ]
        },
        {
            'title': '工作报告',
            'href': '',
            'icon': '&#xe649;',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '工作日报',
                    'href': 'menu/report/report.html',
                    'fontFamily': 'layui-icon',
                    'spread': False
                }
            ]
        },
        {
            'title': '人事管理',
            'href': '',
            'icon': '&#xe66f;',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '员工管理',
                    'href': 'menu/user/user.html',
                    'spread': False},
                {
                    'display': True,
                    'title': '部门管理',
                    'href': 'menu/user/department.html',
                    'spread': False
                }
            ]
        },
        {
            'title': '知识库',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe7c5;',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '知识广场',
                    'href': 'menu/repository/repository.html',
                    'spread': False
                },
                {
                    'display': True,
                    'title': '我的文章',
                    'href': 'menu/repository/myrepository.html',
                    'spread': False
                }
            ]
        },
        {
            'title': '解析工具',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': 'ok-icon ok-icon-repair',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '日志解析',
                    'href': 'menu/tools/analyze-log.html',
                    'spread': False
                }
            ]
        },
        {
            'title': '系统设置',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe68a;',
            'spread': False,
            'display': True,
            'children': [
                {
                    'display': True,
                    'title': '个人设置',
                    'href': 'menu/setting/user-setting.html',
                    'spread': False},
                {
                    'display': True,
                    'title': '安全设置',
                    'href': 'menu/setting/user-security.html',
                    'spread': False
                },
                {
                    'display': True if _ else False,
                    'title': '系统设置',
                    'href': 'menu/setting/setting.html',
                    'spread': False
                }
            ]
        }
    ]


public()
