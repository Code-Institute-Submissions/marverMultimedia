# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-23 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager_app', '0010_eventrating_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='event_title',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AddField(
            model_name='support',
            name='event_title',
            field=models.CharField(default=None, max_length=300),
        ),
    ]
