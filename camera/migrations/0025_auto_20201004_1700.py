# Generated by Django 3.1 on 2020-10-04 17:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0024_modelanalysis_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 4, 17, 0, 10, 79434, tzinfo=utc)),
        ),
    ]
