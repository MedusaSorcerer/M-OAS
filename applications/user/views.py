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


def get_permission(role: list, a_index, b_index=None):
    try:
        permission = role[a_index]
        return permission['spread'] if b_index is None else permission['children'][b_index]['spread']
    except (Exception,):
        return False


def navs(role):
    role = json.loads(role)
    return [
        {
            'title': 'Dashboard',
            'href': 'menu/dashboard/dashboard.html',
            'fontFamily': 'ok-icon',
            'icon': '&#xe61b;',
            'spread': True,
            'isCheck': True,
            'display': True,
            'id': 'm/1',
        },
        {
            'title': '流程处理',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe6d7;',
            'display': get_permission(role, 1),
            'id': 'm/2',
            'children': [
                {
                    'display': get_permission(role, 1, 0),
                    'title': '我提交的流程',
                    'href': 'menu/process/submitProcess.html',
                    'spread': False,
                    'id': 'm/2/1',
                },
                {
                    'display': get_permission(role, 1, 1),
                    'title': '我处理的流程',
                    'href': 'menu/process/handleProcess.html',
                    'spread': False,
                    'id': 'm/2/2',
                }
            ]
        },
        {
            'title': '考勤处理',
            'fontFamily': 'ok-icon',
            'icon': '&#xe640;',
            'spread': False,
            'display': get_permission(role, 2),
            'id': 'm/3',
            'children': [
                {
                    'display': get_permission(role, 2, 0),
                    'title': '个人考勤',
                    'href': 'menu/attendance/attendance.html',
                    'spread': False,
                    'id': 'm/3/1',
                }
            ]
        },
        {
            'title': '工作报告',
            'href': '',
            'icon': '&#xe649;',
            'spread': False,
            'display': get_permission(role, 3),
            'id': 'm/4',
            'children': [
                {
                    'display': get_permission(role, 3, 0),
                    'title': '工作日报',
                    'href': 'menu/report/report.html',
                    'fontFamily': 'layui-icon',
                    'spread': False,
                    'id': 'm/4/1',
                },
                {
                    'display': get_permission(role, 3, 1),
                    'title': '工作月报',
                    'href': 'menu/report/monthlyReport.html',
                    'fontFamily': 'layui-icon',
                    'spread': False,
                    'id': 'm/4/2',
                },
                {
                    'display': get_permission(role, 3, 2),
                    'title': '项目工程',
                    'href': 'menu/report/subject.html',
                    'fontFamily': 'layui-icon',
                    'spread': False,
                    'id': 'm/4/3',
                }
            ]
        },
        {
            'title': '人事管理',
            'href': '',
            'icon': '&#xe66f;',
            'spread': False,
            'display': get_permission(role, 4),
            'id': 'm/5',
            'children': [
                {
                    'display': get_permission(role, 4, 0),
                    'title': '员工管理',
                    'href': 'menu/user/user.html',
                    'spread': False,
                    'id': 'm/5/1',
                },
                {
                    'display': get_permission(role, 4, 1),
                    'title': '角色管理',
                    'href': 'menu/user/role.html',
                    'spread': False,
                    'id': 'm/5/3',
                },
                {
                    'display': get_permission(role, 4, 2),
                    'title': '部门管理',
                    'href': 'menu/user/department.html',
                    'spread': False,
                    'id': 'm/5/2',
                },
            ]
        },
        {
            'title': '知识库',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe7c5;',
            'spread': False,
            'display': get_permission(role, 5),
            'id': 'm/6',
            'children': [
                {
                    'display': get_permission(role, 5, 0),
                    'title': '知识广场',
                    'href': 'menu/repository/repository.html',
                    'spread': False,
                    'id': 'm/6/1',
                },
                {
                    'display': get_permission(role, 5, 1),
                    'title': '我的文章',
                    'href': 'menu/repository/myrepository.html',
                    'spread': False,
                    'id': 'm/6/2',
                }
            ]
        },
        {
            'title': '解析工具',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': 'ok-icon ok-icon-repair',
            'spread': False,
            'display': get_permission(role, 6),
            'id': 'm/7',
            'children': [
                {
                    'display': get_permission(role, 6, 0),
                    'title': '日志解析',
                    'href': 'menu/tools/analyze-log.html',
                    'spread': False,
                    'id': 'm/7/1',
                }
            ]
        },
        {
            'title': '系统设置',
            'href': '',
            'fontFamily': 'ok-icon',
            'icon': '&#xe68a;',
            'spread': False,
            'display': get_permission(role, 7),
            'id': 'm/8',
            'children': [
                {
                    'display': get_permission(role, 7, 0),
                    'title': '个人设置',
                    'href': 'menu/setting/user-setting.html',
                    'spread': False,
                    'id': 'm/8/1',
                },
                {
                    'display': get_permission(role, 7, 1),
                    'title': '安全设置',
                    'href': 'menu/setting/user-security.html',
                    'spread': False,
                    'id': 'm/8/2',
                },
                {
                    'display': get_permission(role, 7, 2),
                    'title': '系统设置',
                    'href': 'menu/setting/setting.html',
                    'spread': False,
                    'id': 'm/8/3',
                }
            ]
        }
    ]


def format_role(role: list, admin: bool = False):
    result = [
        {
            # 'title': 'Dashboard',
            'spread': True,
            'id': 'm/1'
        },
        {
            # 'title': '流程处理',
            'spread': 'm/2' in role or admin,
            'id': 'm/2',
            'children': [
                {
                    # 'title': '我提交的流程',
                    'spread': ('m/2' in role and 'm/2/1' in role) or admin,
                    'id': 'm/2/1'
                },
                {
                    # 'title': '我处理的流程',
                    'spread': ('m/2' in role and 'm/2/2' in role) or admin,
                    'id': 'm/2/2'
                }
            ]
        },
        {
            # 'title': '考勤处理',
            'spread': 'm/3' in role or admin,
            'id': 'm/3',
            'children': [
                {
                    # 'title': '个人考勤',
                    'spread': ('m/3' in role and 'm/3/1' in role) or admin,
                    'id': 'm/3/1'
                }
            ]
        },
        {
            # 'title': '工作报告',
            'spread': 'm/4' in role or admin,
            'id': 'm/4',
            'children': [
                {
                    # 'title': '工作日报',
                    'spread': ('m/4' in role and 'm/4/1' in role) or admin,
                    'id': 'm/4/1'
                },
                {
                    # 'title': '工作月报',
                    'spread': ('m/4' in role and 'm/4/2' in role) or admin,
                    'id': 'm/4/2'
                },
                {
                    # 'title': '项目工程',
                    'spread': ('m/4' in role and 'm/4/3' in role) or admin,
                    'id': 'm/4/3'
                }
            ]
        },
        {
            # 'title': '人事管理',
            'spread': 'm/5' in role or admin,
            'id': 'm/5',
            'children': [
                {
                    # 'title': '员工管理',
                    'spread': ('m/5' in role and 'm/5/1' in role) or admin,
                    'id': 'm/5/1'
                },
                {
                    # 'title': '角色管理',
                    'spread': ('m/5' in role and 'm/5/3' in role) or admin,
                    'id': 'm/5/3'
                },
                {
                    # 'title': '部门管理',
                    'spread': ('m/5' in role and 'm/5/2' in role) or admin,
                    'id': 'm/5/2'
                }
            ]
        },
        {
            # 'title': '知识库',
            'spread': 'm/6' in role or admin,
            'id': 'm/6',
            'children': [
                {
                    # 'title': '知识广场',
                    'spread': ('m/6' in role and 'm/6/1' in role) or admin,
                    'id': 'm/6/1'
                },
                {
                    # 'title': '我的文章',
                    'spread': ('m/6' in role and 'm/6/2' in role) or admin,
                    'id': 'm/6/2'
                }
            ]
        },
        {
            # 'title': '解析工具',
            'spread': 'm/7' in role or admin,
            'id': 'm/7',
            'children': [
                {
                    # 'title': '日志解析',
                    'spread': ('m/7' in role and 'm/7/1' in role) or admin,
                    'id': 'm/7/1'
                }
            ]
        },
        {
            # 'title': '系统设置',
            'spread': 'm/8' in role or admin,
            'id': 'm/8',
            'children': [
                {
                    # 'title': '个人设置',
                    'spread': ('m/8' in role and 'm/8/1' in role) or admin,
                    'id': 'm/8/1'
                },
                {
                    # 'title': '安全设置',
                    'spread': ('m/8' in role and 'm/8/2' in role) or admin,
                    'id': 'm/8/2'
                },
                {
                    # 'title': '系统设置',
                    'spread': ('m/8' in role and 'm/8/3' in role) or admin,
                    'id': 'm/8/3'
                }
            ]
        }
    ]
    return json.dumps(result, ensure_ascii=False)


public()
