# Generated by Django 3.1 on 2020-09-16 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0011_auto_20200915_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
    ]
