# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20170621_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='pv',
            field=models.IntegerField(default=0),
        ),
    ]