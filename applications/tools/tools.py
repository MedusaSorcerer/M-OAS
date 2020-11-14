#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import linecache
import os
import time
from datetime import datetime
from uuid import uuid1

import ujson
from django.core.cache import cache

from MOAS.settings import BASE_DIR
from conf.conf import CACHE_TIMEOUT
from lib import m_rest_framework as rest
from lib.parse.parse import parse
from . import tasks

NAME = 'M&OAS_Tools'
TASKS = tasks


def analyze_text(name, line, limit, fields, regex):
    def _(text):
        _result = {}
        search_dict = parse(regex, text)
        for _i in fields.keys():
            if search_dict:
                try:
                    _value = search_dict[str(_i)]
                except KeyError:
                    _value = ''
            else:
                _value = ''
            if isinstance(_value, datetime):
                _value = _value.strftime('%Y-%m-%d %H:%M:%S')
            _result[str(_i)] = _value
        _result['__all__'] = text
        return _result

    count, data = 0, list()
    path = os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{name}.py')
    if os.path.getsize(path) > 1024 ** 3:
        with open(path, 'r', encoding='UTF-8') as f:
            for i in f:
                count += 1
            f.close()
        for i in range(limit):
            line += 1
            if line > count: break
            line_text = linecache.getline(path, line)
            data.append(_(line_text))
    else:
        with open(path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            f.close()
        count = len(lines)
        for i in lines[line: limit + line]:
            data.append(_(i))
    return data, count


def analyze_json(name, line, limit):
    with open(os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{name}.py'), 'r', encoding='UTF-8') as f:
        info = f.read()
        f.close()
    srcdata = ujson.loads(info)
    data = srcdata[line:limit]
    if srcdata and not data: raise rest.NotFound
    result = []
    for i in data:
        src = ujson.dumps(i)
        i.update({'__all__': src})
        result.append(i)
    return result, len(srcdata)


def analyze_engine(tool, limit, page, fields, regex):
    type_, name, line = tool['type'], tool['name'], (page - 1) * limit
    if type_ == 'json':
        data, count = analyze_json(name, line, line + limit)
    else:
        data, count = analyze_text(name, line, limit, fields, regex)
    return data, count


class AnalyzeTool(rest.GenericViewSet):
    def create(self, request, *args, **kwargs):
        file, name, type_, fields, alias, regex = (
            request.FILES.get('file'), str(uuid1()).replace('-', ''),
            request.data.get('type'), request.data.get('fields'),
            request.data.get('alias'), request.data.get('regex'),
        )
        if file:
            try:
                fields = ujson.loads(fields)
            except ValueError:
                raise rest.ParseError(detail='字段映射错误')
            if not isinstance(fields, dict): raise rest.ParseError(detail='字段映射错误')
            f = open(os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{name}.py'), 'w', encoding='UTF-8')
            while text := file.read(10240):
                f.write(text.decode().replace('\r\n', '\n'))
            f.close()
            file.close()
            tools = cache.get(NAME, {})
            tools[f'{request.user.id}{name}'] = {
                'timeout': time.time(),
                'name': name,
                'type': type_,
                'stat': True,
                'fields': fields,
                'alias': alias,
                'regex': regex,
            }
            cache.set(NAME, tools, timeout=CACHE_TIMEOUT)
            return rest.Response(status=200)
        raise rest.ParseError(detail='没有发现上传文件')

    def list(self, request, *args, **kwargs):
        data, timeout, tools, d = [], time.time(), cache.get(NAME, {}), []
        for k, v in tools.items():
            if timeout - v['timeout'] <= CACHE_TIMEOUT and k.startswith(str(request.user.id)):
                fields = {str(k): str(v) for k, v in v['fields'].items()}
                fields['__all__'] = '原数据'
                data.append({
                    'id': v['name'],
                    'fields': fields,
                    'name': v['alias'],
                    'type': v['type'],
                    'regex': v['regex'],
                })
            else:
                try:
                    d.append(f'{request.user.id}{v["name"]}')
                    os.remove(os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{v["name"]}'))
                except (Exception,):
                    pass
        if d: [tools.pop(i, '') for i in d]
        cache.set(NAME, tools, timeout=CACHE_TIMEOUT)
        return rest.Response(data=data)

    def retrieve(self, request, *args, **kwargs):
        timeout, tools, limit, page = (
            time.time(),
            cache.get(NAME, {}),
            request.query_params.get('limit', '20'),
            request.query_params.get('page', '1'),
        )
        tool = tools.get(f'{request.user.id}{kwargs.get("pk")}')
        if not limit.isdigit() or not page.isdigit(): raise rest.ParseError(detail='分页参数错误')
        limit, page = int(limit), int(page)
        if limit < 0 or limit > 100 or page < 1: raise rest.ParseError(detail='分页参数错误')
        if not tool: raise rest.NotFound
        if timeout - tool['timeout'] >= CACHE_TIMEOUT:
            try:
                os.remove(os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{tool["name"]}'))
                tools.pop(f'{request.user.id}{kwargs.get("pk")}')
                cache.set(NAME, tools, timeout=CACHE_TIMEOUT)
            except (Exception,):
                pass
            raise rest.NotFound
        data, count = analyze_engine(tool, limit, page, tool['fields'], tool['regex'])
        return rest.Response(data=data, count=count)


class ManagementMappingRulerView(rest.GenericViewSet, rest.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        type_, regex, fields, name = request.data.get('type'), request.data.get('regex'), request.data.get('fields'), kwargs.get('pk')
        tools = cache.get(NAME, {})
        tool = tools.get(f'{request.user.id}{name}')
        if not tool: raise rest.NotFound
        try:
            fields = ujson.loads(fields)
        except ValueError:
            raise rest.ParseError(detail='字段映射错误')
        if not isinstance(fields, dict): raise rest.ParseError(detail='字段映射错误')
        tool.update({
            'timeout': time.time(),
            'type': type_,
            'fields': fields,
            'regex': regex,
        })
        tools[f'{request.user.id}{name}'] = tool
        cache.set(NAME, tools, timeout=CACHE_TIMEOUT)
        return rest.Response(data={'type': type_, 'fields': fields, 'regex': regex})
