# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20170622_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='pv',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]