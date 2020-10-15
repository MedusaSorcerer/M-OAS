#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from django.db import models

from applications.user.models import UserModel


class RepositoryModel(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField()
    update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'moas_repository'
        ordering = ('-id',)
