# Generated by Django 3.1.1 on 2020-09-24 01:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200916_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='paid_leave',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('fa85f306-4d12-4da8-ab00-508d0f387138')),
        ),
    ]
