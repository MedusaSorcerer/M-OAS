#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models
from django.utils.deconstruct import deconstructible

from .views import workplace as get_workplace


@deconstructible
class PhoneRegexValidator(validators.RegexValidator):
    regex = r'^1[34589]\d{9}$'
    message = '手机号码格式错误'
    flags = 0


class RoleModel(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    role = models.CharField(max_length=128, null=False, blank=False)
    create = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'moas_role'
        ordering = ('-id',)


class DepartmentModel(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'moas_department'
        ordering = ('-id',)


class UserModel(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    phone_validator = PhoneRegexValidator

    username = models.CharField(
        max_length=32,
        unique=True,
        validators=[username_validator],
        error_messages={'unique': "A user with that username already exists."},
    )
    is_admin = models.BooleanField(default=False)
    user_secret = models.UUIDField(default=uuid4())
    email = models.EmailField(blank=True, null=True)
    role = models.ManyToManyField(RoleModel)
    head_of_department = models.BooleanField(default=False)
    work_management = models.BooleanField(default=False)
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(null=True, validators=[phone_validator], max_length=11)
    workplace = models.CharField(null=True, max_length=32)
    title = models.CharField(null=True, max_length=32)
    paid_leave = models.IntegerField(default=0)

    def is_administrator(self):
        return True if self.role.filter(name__exact='Administrator') else False

    def get_workplace(self):
        if not self.workplace: return None, None
        a, b = self.workplace.split('/')
        workplace = get_workplace(f=True)
        return workplace.get(a, {}).get('code'), workplace.get(a, {}).get('children', {}).get(b, {}).get('code')[len(a):]

    class Meta:
        db_table = 'moas_user'
        ordering = ('-id',)

    def get_full_name(self):
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        elif self.first_name:
            full_name = self.first_name
        else:
            full_name = self.last_name
        return full_name.strip()


def _():
    def _():
        import time
        time.sleep(2)
        try:
            from conf import conf
            if not UserModel.objects.filter(is_admin__exact=True):
                UserModel.objects.create_user(
                    username=conf.ADMIN_USERNAME,
                    password=conf.ADMIN_PASSWORD,
                    email=conf.ADMIN_EMAIL,
                    is_admin=True,
                )
        except (Exception,):
            pass

    import _thread
    _thread.start_new_thread(_, ())

_()
