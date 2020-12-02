from django.db import models
from djcelery.models import PeriodicTasks, CrontabSchedule, PeriodicTask

from applications.user.models import UserModel

CrontabModel = PeriodicTask
CrontabSignModel = PeriodicTasks
CrontabTimerModel = CrontabSchedule


def _():
    from applications.user.models import UserModel
    return UserModel.objects.filter(is_admin__exact=True).first().id


class ScriptModel(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    uploader = models.ForeignKey(UserModel, on_delete=models.SET(_))
    params = models.TextField(default='{}')
    uuid = models.UUIDField()
    status = models.BooleanField(default=False)
    use = models.BooleanField(default=False)
    upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moas_script'
        ordering = ('-id',)


class TasksModel(models.Model):
    creator = models.ForeignKey(UserModel, on_delete=models.SET(_))
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    script = models.ForeignKey(ScriptModel, on_delete=models.CASCADE)
    params = models.ForeignKey
