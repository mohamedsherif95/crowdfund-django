# Generated by Django 3.2.9 on 2021-12-06 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_rename_images_project_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='img',
            new_name='images',
        ),
        migrations.AlterField(
            model_name='image',
            name='project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='im', to='projects.project'),
        ),
    ]
