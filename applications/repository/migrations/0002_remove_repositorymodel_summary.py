# Generated by Django 3.1.1 on 2020-10-13 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repositorymodel',
            name='summary',
        ),
    ]