# Generated by Django 3.1 on 2020-09-07 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20200907_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='processmodel',
            name='protype',
            field=models.IntegerField(choices=[(0, '堡垒机'), (1, '考勤'), (2, '网络开墙'), (3, '其他')], default=1),
            preserve_default=False,
        ),
    ]
