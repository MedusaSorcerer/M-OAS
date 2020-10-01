# Generated by Django 3.1.1 on 2020-09-15 02:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_auto_20200909_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processmodel',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='processmodel',
            name='protype',
            field=models.IntegerField(choices=[(0, '堡垒机'), (1, '考勤'), (2, '网络开墙'), (3, '请求假期'), (4, '其他')]),
        ),
    ]
