# Generated by Django 3.1 on 2020-09-14 11:08

import camera.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0008_auto_20200914_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_media',
            field=models.FileField(default='', upload_to=camera.models.path_and_rename),
        ),
    ]