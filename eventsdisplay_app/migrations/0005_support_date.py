# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-15 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventsdisplay_app', '0004_support_issuetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
