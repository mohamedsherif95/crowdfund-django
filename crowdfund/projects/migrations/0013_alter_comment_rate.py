# Generated by Django 3.2.9 on 2021-12-03 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_comment_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='1', max_length=2),
        ),
    ]
