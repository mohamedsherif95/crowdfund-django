# Generated by Django 3.2.9 on 2021-11-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211122_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='avatar.png', null=True, upload_to=''),
        ),
    ]