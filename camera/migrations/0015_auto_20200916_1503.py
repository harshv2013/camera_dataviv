# Generated by Django 3.1 on 2020-09-16 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0014_auto_20200916_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='owner',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.DO_NOTHING, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
    ]
