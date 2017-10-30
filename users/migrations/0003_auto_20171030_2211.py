# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171030_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userext',
            name='nickname',
            field=models.CharField(blank=True, max_length=64, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='userext',
            name='validkey',
            field=models.CharField(blank=True, max_length=256, verbose_name='验证key'),
        ),
    ]
