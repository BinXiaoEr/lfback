# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-18 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sing', '0003_auto_20200418_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singinfo',
            name='sing_id',
            field=models.IntegerField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
