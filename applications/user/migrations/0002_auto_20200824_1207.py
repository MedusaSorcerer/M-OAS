# Generated by Django 3.0.6 on 2020-08-24 04:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('2a98db1e-e45f-412e-9aee-a2fbfaae502a')),
        ),
    ]
