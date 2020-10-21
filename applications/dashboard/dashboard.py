#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import datetime

from django.core.cache import cache
from django.db import connection
from django.db.models import Count

from applications.process.models import ProcessModel
from applications.report.models import ReportModel
from applications.repository.models import RepositoryModel
from applications.user.models import UserModel
from lib import m_rest_framework as rest


def overview():
    return [
        ProcessModel.objects.count(),
        ReportModel.objects.count(),
        RepositoryModel.objects.count(),
        UserModel.objects.count(),
    ]


def overview_detail():
    def _overview_detail(model, field):
        select, day, result, today = (
            {'day': connection.ops.date_trunc_sql('day', f'`{field}`')},
            (datetime.datetime.now() + datetime.timedelta(days=-6)).date(),
            [0, 0, 0, 0, 0, 0, 0],
            datetime.datetime.now().date(),
        )
        queryset = model.objects.filter(**{f'{field}__gte': str(day)}).extra(select=select).values('day').annotate(count=Count('id')).order_by('day')
        for i in queryset:
            result[(today - i['day']).days] = i['count']
        return result[::-1]

    return {
        'process': _overview_detail(ProcessModel, 'create_time'),
        'report': _overview_detail(ReportModel, 'date'),
        'repository': _overview_detail(RepositoryModel, 'update'),
        'user': _overview_detail(UserModel, 'date_joined'),
    }


def useractive():
    _ = datetime.datetime.now()
    result = list()
    for i in range(7):
        sign = (_ + datetime.timedelta(days=-i)).strftime('%Y%m%d')
        dcache = cache.get(f'M&OAS-User-Active-Dcacch-{sign}', [])
        result.append(len(set(dcache)))
    return result[::-1]


def attendance():
    return [
        {'name': '正常', 'value': 23},
        {'name': '早退', 'value': 1},
        {'name': '迟到', 'value': 1},
    ]


class DashboardView(rest.APIView):
    def get(self, request, *args, **kwargs):
        return rest.Response(
            overview=overview(),
            overview_detail=overview_detail(),
            useractive=useractive(),
            attendance=attendance(),
        )
