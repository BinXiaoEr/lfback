# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-20 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongInfo',
            fields=[
                ('song_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='标题')),
                ('img', models.CharField(blank=True, max_length=255, null=True, verbose_name='图片地址')),
                ('author_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='作者')),
                ('album_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='专辑')),
                ('album_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='专辑id')),
                ('album_img', models.TextField(blank=True, null=True, verbose_name='专辑img')),
                ('play_id', models.CharField(max_length=255, null=True, verbose_name='歌单id')),
                ('author_two', models.CharField(blank=True, max_length=10, null=True)),
                ('author_three', models.CharField(blank=True, max_length=10, null=True)),
                ('author_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sing.SingInfo')),
            ],
        ),
        migrations.CreateModel(
            name='SongTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='名称')),
            ],
        ),
    ]
