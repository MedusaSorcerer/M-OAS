# Generated by Django 3.1.1 on 2020-11-19 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_subjectmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectmodel',
            name='version',
        ),
        migrations.AddField(
            model_name='subjectmodel',
            name='accomplish',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='subjectmodel',
            name='establish',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='VersionManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='0.0.1', max_length=64)),
                ('document', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.subjectmodel')),
            ],
            options={
                'db_table': 'moas_version_management',
            },
        ),
    ]