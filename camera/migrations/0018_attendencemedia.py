# Generated by Django 3.1 on 2020-09-28 12:48

import camera.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0017_attendence'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendenceMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendence_media', models.FileField(upload_to=camera.models.path_and_rename2)),
            ],
        ),
    ]
