#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from lib import m_rest_framework as rest


class DashboardView(rest.APIView):
    def get(self, request, *args, **kwargs):
        return rest.Response(
            overview=[34, 103, 65, 101],
            overview_detail={
                'process': [1, 2, 4, 8, 4, 1, 4],
                'report': [3, 10, 3, 2, 1, 9, 0],
                'repository': [5, 10, 3, 3, 0, 5, 1],
                'user': [0, 1, 1, 3, 1, 0, 0]
            },
            useractive=[22, 40, 64, 13, 55, 20, 50],
            attendance=[
                {'name': '正常', 'value': 23},
                {'name': '早退', 'value': 1},
                {'name': '迟到', 'value': 1},
            ]
        )
