#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from django.db import models
from django.utils import timezone

from applications.user.models import UserModel


class ProcessModel(models.Model):
    UNASSIGNED = 0
    OPEN = 1
    DENY = 2
    APPROVE = 3
    CLOSE = 4
    STATUS = ((UNASSIGNED, '未分配'), (OPEN, '打开'), (DENY, '已拒绝'), (APPROVE, '已批准'), (CLOSE, '已关闭'))

    T1 = 0
    T2 = 1
    T3 = 2
    T4 = 3
    T5 = 4
    PROTYPE = ((T1, '堡垒机'), (T2, '考勤'), (T3, '网络开墙'), (T4, '请休假期'), (T5, '其他'))

    title = models.CharField(max_length=64, null=False, blank=False)
    organizer = models.ForeignKey(UserModel, null=False, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    at_leader = models.CharField(max_length=64, null=True, blank=True)
    demand = models.CharField(max_length=512)
    status = models.IntegerField(choices=STATUS)
    content = models.TextField(default='[]')
    protype = models.IntegerField(choices=PROTYPE)

    class Meta:
        db_table = 'moas_process'
        ordering = ('-create_time',)
