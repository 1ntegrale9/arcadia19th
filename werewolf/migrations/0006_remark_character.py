# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-03 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('werewolf', '0005_auto_20170903_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='remark',
            name='character',
            field=models.IntegerField(default=1),
        ),
    ]