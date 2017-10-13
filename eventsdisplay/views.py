# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import datetime

# Create your views here.

def home_page(request):
    upcoming_webcasts = Webcast.objects.all().filter(webcast_date__gte=datetime.date.today())
    archived_webcasts = Webcast.objects.all().filter(webcast_date__lte = datetime.date.today())[:6]

    return render(request, "eventsdisplay_templates/home.html", {'webcasts':upcoming_webcasts , 'archived_webcasts':archived_webcasts})
