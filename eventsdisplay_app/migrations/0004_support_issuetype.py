# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-15 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventsdisplay_app', '0003_eventrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='issueType',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
