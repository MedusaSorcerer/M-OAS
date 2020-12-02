#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import json
import os
import re

from MOAS.settings import BASE_DIR
from applications.user.user import rsa_decrypt
from applications.user.views import workplace as get_workplace
from lib import m_rest_framework as rest


class PersonalSettingSerializer(rest.Serializer):
    full_name = rest.CharField(max_length=32, allow_null=False)
    email = rest.EmailField(max_length=62, allow_null=False)
    phone = rest.IntegerField(allow_null=False)
    jobnumber = rest.CharField(max_length=5, allow_null=False)
    workplace = rest.CharField(max_length=5, allow_null=False)

    def validate_phone(self, attrs):
        if not re.match(r'^1[34589]\d{9}$', str(attrs)):
            raise rest.ValidationError('手机号码不合法')
        return attrs

    def validate(self, attrs):
        file = get_workplace(True)
        if workplace := attrs.get('workplace'):
            if not file.get(workplace):
                raise rest.ValidationError('职场编号不合法')
            if jobnumber := attrs.get('jobnumber'):
                jobnumber = jobnumber[len(workplace):]
                if not file.get(workplace)['children'].get(jobnumber):
                    raise rest.ValidationError('工位编号不合法')
                attrs['jobnumber'] = jobnumber
        else:
            attrs['jobnumber'] = ''
        return attrs


class PersonalSettingView(rest.APIView):
    permission = {'m/8/1': '__all__'}

    def get(self, request, *args, **kwargs):
        instance = request.user
        a, b = instance.get_workplace()
        return rest.Response(
            data={
                'email': instance.email,
                'username': instance.username,
                'full_name': instance.get_full_name(),
                'workplace_a': a if a else '',
                'workplace_b': a + b if a and b else '',
                'phone': instance.phone,
                'paid_leave': instance.paid_leave,
            },
            workplace=get_workplace(),
        )

    def put(self, request, *args, **kwargs):
        serializer = PersonalSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.email = serializer.data.get('email')
        user.phone = serializer.data.get('phone')
        user.last_name = serializer.data.get('full_name')
        user.first_name = ''
        user.workplace = f'{serializer.data.get("workplace")}/{serializer.data.get("jobnumber")}'
        user.save()
        return rest.Response(data=request.data)


class SecuritySettingView(rest.APIView):
    permission = {'m/8/2': '__all__'}

    def get(self, request, *args, **kwargs):
        return rest.Response(data={'username': request.user.username})


class SystemSettingView(rest.APIView):
    permission = {'m/8/3': '__all__'}

    def get(self, request, *args, **kwargs):
        file = open(os.path.join(BASE_DIR, 'conf', 'conf.json'), 'r', encoding='UTF-8')
        info = file.read()
        file.close()
        jinfo = json.loads(info)
        workplace = {i['name']: [i2['name'] for i2 in i['children']] for i in get_workplace()}
        return rest.Response(data={
            'email-address': jinfo.get('email-address'),
            'system-email': jinfo.get('system-email'),
            'workplace': json.dumps(workplace, indent=4, ensure_ascii=False)
        })

    def put(self, request, *args, **kwargs):
        data, index = request.data, 0
        try:
            workplace = json.loads(data.get('workplace', '{}'))
        except json.decoder.JSONDecodeError:
            raise rest.ParseError(detail='工位录入数据无法解析')
        if not isinstance(workplace, dict): raise rest.ParseError(detail='工位录入数据无法解析')
        www = dict()
        for key, value in workplace.items():
            if not isinstance(value, list): raise rest.ParseError(detail='工位录入数据无法解析')
            children = dict()
            for i, v in enumerate(value):
                if not isinstance(v, (str, int)): raise rest.ParseError(detail='工位录入数据无法解析')
                children[str(i)] = {'code': f'{index}{i}', 'name': str(v)}
            www[str(index)] = {
                'code': str(index),
                'name': key,
                'children': children,
            }
            index += 1
        try:
            password = rsa_decrypt(data.get('system-email-pwd'))
        except (ValueError, AttributeError):
            raise rest.ParseError(detail='密码无法验证')
        file = open(os.path.join(BASE_DIR, 'conf', 'conf.json'), 'r', encoding='UTF-8')
        info = file.read()
        file.close()
        jinfo = json.loads(info)
        file = open(os.path.join(BASE_DIR, 'conf', 'conf.json'), 'w', encoding='UTF-8')
        file2 = open(os.path.join(BASE_DIR, 'applications', 'user', 'workplace.json'), 'w', encoding='UTF-8')
        if password == 'HiddenPassword':
            jinfo.update({
                'email-address': data.get('email-address'),
                'system-email': data.get('system-email')
            })
        else:
            jinfo.update({
                'email-address': data.get('email-address'),
                'system-email': data.get('system-email'),
                'system-email-pwd': password,
            })
        file.write(json.dumps(jinfo))
        file2.write(json.dumps(www))
        file.close()
        file2.close()
        return rest.Response(data={'email-address': data.get('email-address'), 'system-email': data.get('system-email')})
