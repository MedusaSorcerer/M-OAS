#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from datetime import datetime, timedelta
from random import randint

from applications.process.models import ProcessModel
from lib import m_rest_framework as rest

HOLIDAY = {
    '1': '年休假',
    '2': '产假',
    '3': '事假',
    '4': '婚假',
    '5': '病假',
    '6': '其他',
}


class AttendanceView(rest.GenericViewSet):
    def list(self, request, *args, **kwargs):
        data = list()
        now = datetime.now()
        for i in range(1, 51):
            date = (now + timedelta(days=-i))
            if date.isoweekday() > 5:
                from_ = to = None
            else:
                from_ = date.replace(hour=8, minute=randint(1, 59), second=randint(1, 59)).strftime("%Y-%m-%d %H:%M:%S")
                to = date.replace(hour=16, minute=randint(1, 59), second=randint(1, 59)).strftime("%Y-%m-%d %H:%M:%S")
            data.append({
                'id': i,
                'date': date.strftime("%Y-%m-%d"),
                'from': from_,
                'to': to,
                'status': 0,
                'account': 'admin',
                'fullname': 'Medusa Sorcerer'
            })
        limit, page = int(request.query_params.get('limit')), int(request.query_params.get('page'))
        a, b = (page - 1) * limit, page * limit
        return rest.Response(data=data[a:b], count=len(data))


class AbnormalAttendanceView(rest.GenericViewSet):
    @staticmethod
    def demo():
        data = list()
        now = datetime.now()
        for i in range(5):
            data.append({
                'id': i,
                'description': f'{(now + timedelta(days=-i)).strftime("%Y-%m-%d")} 上午'
            })
        return data

    def list(self, request, *args, **kwargs):
        return rest.Response(data=self.demo())

    def create(self, request, *args, **kwargs):
        # TODO 省略数据校验
        ProcessModel.objects.create(
            title='考勤异常申请',
            organizer=request.user,
            at_leader='"' + str(request.user.department.usermodel_set.all().filter(work_management__exact=True).first().id) + '"',
            demand=f'{request.data.get("demand")} ({self.demo()[int(request.data.get("time"))]["description"]})',
            status=ProcessModel.OPEN,
            protype=ProcessModel.T2,
        )
        return rest.Response(data={'demand': request.data.get("demand"), 'time': request.data.get("time")}, status=rest.HTTP_201_CREATED)


class HolidayHandleView(rest.GenericViewSet):
    def list(self, request, *args, **kwargs):
        return rest.Response(data=[{'id': k, 'name': v} for k, v in HOLIDAY.items()])

    def get_time(self, key1, key2):
        _time = {'1': '09:00:00', '2': '14:00:00', '3': '12:00:00', '4': '16:00:00'}.get(key2)
        if not _time: raise rest.ParseError(detail='时间格式无法识别')
        _datetime = f'{key1} {_time}'
        try:
            _ = datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise rest.ParseError(detail='时间格式无法识别')
        return _datetime, _

    def create(self, request, *args, **kwargs):
        title, protype, organizer_id, status = '假期请休申请', ProcessModel.T4, request.user.id, ProcessModel.OPEN
        at_leader = '"' + str(request.user.department.usermodel_set.all().filter(work_management__exact=True).first().id) + '"'
        (starttime, _s), (endtime, _e) = (
            self.get_time(request.data.get('startDate'), request.data.get('startTime')),
            self.get_time(request.data.get('endDate'), request.data.get('endTime')),
        )
        print(starttime, endtime)
        if starttime > endtime: raise rest.ParseError(detail='时间区间不合法')
        n = (_e - _s).days
        if request.data.get('startTime') == '1' and request.data.get('endTime') == '3':
            n += .5
        else:
            n += 1
        demand = request.data.get('demand') + f'\n\n系统数据：\n    请休假期时间为 {starttime} 至 {endtime}，共计 {n} 天。'
        if request.data.get('holiday') == '1':
            if request.user.paid_leave < n: raise rest.ParseError(detail='申请不通过，剩余年假小于请休时间。')
            demand += f'\n    当前申请者剩余年休假为 {request.user.paid_leave} 天'
        _ = ProcessModel.objects.create(
            title=title,
            organizer_id=organizer_id,
            at_leader=at_leader,
            demand=demand,
            status=status,
            protype=protype,
        )
        return rest.Response(data=dict(
            id=_.id,
            title=title,
            organizer_id=organizer_id,
            at_leader=at_leader,
            demand=demand,
            status=status,
            protype=protype
        ))
