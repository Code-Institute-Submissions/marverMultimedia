# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import *

def eventsmanager(request):
    webcast_list = Webcast.objects.all()
    current_url = request.build_absolute_uri()
    edit_url = current_url.replace('/administration/', '')
    return render(request,'eventsmanager_app_templates/events_manager.html',{'webcasts': webcast_list,'current_url':edit_url})

