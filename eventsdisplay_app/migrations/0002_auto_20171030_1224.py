# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventsdisplay_app', '0001_initial'),
        ('eventsmanager_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='webcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventsmanager_app.Webcast'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='webcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventsmanager_app.Webcast'),
        ),
    ]