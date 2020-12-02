#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from django.db import models

from applications.user.models import UserModel, DepartmentModel


class ReportModel(models.Model):
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moas_report'
        ordering = ('-id',)


class MonthlyReportModel(models.Model):
    person = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.CharField(max_length=6, null=False, blank=False)
    schedule = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moas_monthly_report'
        ordering = ('-update', '-id')


class SubjectModel(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    schedule = models.IntegerField(default=0)
    team = models.CharField(max_length=64, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    pertain = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    establish = models.DateField(null=True)
    accomplish = models.DateField(null=True)

    class Meta:
        db_table = 'moas_subject'
        ordering = ('-update', '-id')


class VersionManagement(models.Model):
    version = models.CharField(max_length=64, default='0.0.1', null=False)
    document = models.TextField()
    subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moas_version_management'
