# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-27 17:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200427_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhistory',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
