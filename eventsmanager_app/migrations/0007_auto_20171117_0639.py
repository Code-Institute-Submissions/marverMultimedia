# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-17 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager_app', '0006_auto_20171116_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='support',
            name='date',
            field=models.DateTimeField(default=None),
        ),
    ]
