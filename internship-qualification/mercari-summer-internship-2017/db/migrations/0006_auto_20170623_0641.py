# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_auto_20170622_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='pv',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
