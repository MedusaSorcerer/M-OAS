# Generated by Django 3.1 on 2020-09-08 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_auto_20200907_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processmodel',
            name='status',
            field=models.IntegerField(choices=[(0, '未分配'), (1, '打开'), (2, '已拒绝'), (3, '已批准'), (4, '已关闭')]),
        ),
    ]
