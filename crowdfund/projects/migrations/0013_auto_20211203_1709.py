# Generated by Django 3.2.9 on 2021-12-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='report_url',
        ),
        migrations.AddField(
            model_name='report',
            name='category',
            field=models.CharField(choices=[('hm', 'Harmful'), ('fk', 'Fake'), ('il', 'Illegale'), ('ab', 'Abuse')], default='fk', max_length=2),
        ),
    ]
