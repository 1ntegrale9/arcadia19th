# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('werewolf', '0022_village_started_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='remark',
            name='nightflag',
            field=models.IntegerField(default=0),
        ),
    ]
