# Generated by Django 3.2.9 on 2021-12-02 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_rename_post_images_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
