#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import ujson

from lib import m_rest_framework as rest


def analyze_json(file):
    try:
        return ujson.load(file)
    except ValueError:
        raise rest.ParseError(detail='JSON 文件格式错误，无法解析')


def analyze_text(file, regex):
    ...


def analyze_excel(text):
    ...


class AnalysisLog(rest.GenericViewSet):
    # FIXME fileType: json | text&regex | excel
    # TODO Search/Datetime/List展示/ajax请求
    ...
