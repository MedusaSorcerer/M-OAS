#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from django.db import models

from applications.user.models import UserModel


class ReportModel(models.Model):
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'moas_report'
        ordering = ('-id',)
