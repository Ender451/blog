# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-create_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
    ]