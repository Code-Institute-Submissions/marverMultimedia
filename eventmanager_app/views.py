# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect
from .models import *
from .forms import *
import boto3

def eventsmanager(request):
    webcast_list = Webcast.objects.all()
    current_url = request.build_absolute_uri()
    edit_url = current_url.replace('/administration/', '')
    return render(request,'eventsmanager_app_templates/events_manager.html',{'webcasts': webcast_list,'current_url':edit_url})

def eventCreation(request):

    if request.method == 'POST':
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/administration/')
    else:
        form = EventCreation()
    webcast_speakers = Speakers.objects.all()

    return render(request, 'eventsmanager_app_templates/event_creation.html', {'form': form, 'speakers':webcast_speakers})

