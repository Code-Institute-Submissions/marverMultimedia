# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import render
from eventsmanager_app.models import *
import datetime


def home_page(request):
    upcoming_webcasts = Webcast.objects.all().filter(webcast_date__gte=datetime.date.today())
    archived_webcasts = Webcast.objects.all().filter(webcast_date__lte = datetime.date.today())[:6]

    return render(request, "eventsdisplay/home.html", {'webcasts':upcoming_webcasts , 'archived_webcasts':archived_webcasts})

def eventslibrary(request):

    events_list = Webcast.objects.all()
    request.build_absolute_uri()
    return render(request, "eventsdisplay/events.html", {'events' : events_list})

def event_player(request,id):
    event_id = get_object_or_404(Webcast, pk=id)
    event_list = Webcast.objects.all().filter(webcast_date__lte=datetime.date.today()).exclude(id__exact = id)
    single_assets_list = Assets.objects.all().filter(webcast__id__contains=id )
    speakers_list = Speakers.objects.all().filter(webcast__id__contains=id)
    try:
        agenda_list = Agenda.objects.get(webcast_id=id)
    except:
        agenda_list = None
    return render(request, "eventsdisplay/player.html", {'webcasts':event_list, 'webcast_id':event_id, 'assets':single_assets_list, 'agenda':agenda_list, 'speakers_list':speakers_list})



