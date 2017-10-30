# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import render,render_to_response
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives,BadHeaderError
from eventsmanager_app.models import *
from eventsdisplay_app.models import Feedback,Support
from django.db import connection
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


def home_page(request):
    upcoming_webcasts = Webcast.objects.all().filter(webcast_date__gte=datetime.date.today())
    archived_webcasts = Webcast.objects.all().filter(webcast_date__lte = datetime.date.today())[:6]

    return render(request, "eventsdisplay/home.html", {'webcasts':upcoming_webcasts , 'archived_webcasts':archived_webcasts})

def eventslibrary(request):

    events_list = Webcast.objects.all().order_by('-webcast_date')
    request.build_absolute_uri()
    return render(request, "eventsdisplay/events.html", {'events' : events_list})

@csrf_exempt
def events_order(request,option):

     if  0  == int(option):
         events_list = Webcast.objects.all().order_by('webcast_date')
         return render(request,"eventsdisplay/events.html",{'events' : events_list})
     else:
         events_list = Webcast.objects.all().filter(webcast_date__month=int(option))
         if len(events_list) > 0:
             return render(request, "eventsdisplay/events.html", {'events': events_list})
         else:
             response = HttpResponse('OOOOps, it seems there were no events on the selected month', content_type="text/plain")
             response.status_code=500
             return response

@csrf_exempt
def search_events(request,search):

    events_list =  Webcast.objects.raw("""SELECT * FROM marver.eventsmanager_app_webcast WHERE webcast_title LIKE concat('%%', %s, '%%'); """,[search])

    try:
        print(events_list[0])
        return render(request,"eventsdisplay/events.html",{'events' : events_list})
    except IndexError:
        response = HttpResponse('OOOOps, your search has not returned any results',
                                content_type="text/plain")
        response.status_code = 500
        return response


def event_player(request,id):
    event_id = get_object_or_404(Webcast, pk=id)
    event_list = Webcast.objects.all().filter(webcast_date__lte=datetime.date.today()).exclude(id__exact = id)
    single_assets_list = Assets.objects.all().filter(webcast__id__contains=id )
    speakers_list = Speakers.objects.all().filter(webcast__id__contains=id)
    try:
        agenda_list = Agenda.objects.get(webcast_id=id)
    except:
        agenda_list = None
    return render(request, "eventsdisplay/player.html", {'webcasts':event_list, 'event_id':event_id, 'assets':single_assets_list, 'agenda':agenda_list, 'speakers_list':speakers_list})


def event_comment(request):
    if request.method == 'POST':
        if request.POST['form'] == "commentForm":
            try:
                name = request.POST['name']
                surname = request.POST['surname']
                email = request.POST['email']
                comment = request.POST['comment']
                webcast_id = request.POST['webcast_id']
                webcast_title = request.POST['webcast_title']

                Feedback.objects.create(
                    name = name,
                    surname = surname,
                    email = email,
                    comment = comment,
                    webcast_id = webcast_id,
                )

                subject, from_email, to = 'Thank you for contacting Marver', 'lucalicata@hotmail.com', email
                text_content = 'This is an important message.'
                context = {
                    'name' : name.upper(),
                    'comment' : comment,
                    'webcast_title' : webcast_title.upper()
                }
                message = get_template('eventsdisplay/comment_email_template.html')
                msg = EmailMultiAlternatives(subject ,text_content, from_email, [to])
                msg.attach_alternative(message.render(context),'text/html')
                msg.send()
                return HttpResponse('You have successfully submitted your feedback, thank you!!')
            except BadHeaderError:
                return HttpResponse('There have been an error please try again')
        else:
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            comment = request.POST['comment']
            webcast_id = request.POST['webcast_id']
            webcast_title = request.POST['webcast_title']

            Support.objects.create(
                name=name,
                surname=surname,
                email=email,
                support_request=comment,
                webcast_id=webcast_id,
            )

            subject, from_email, to = 'Thank you for your support request', 'lucalicata@hotmail.com', email
            text_content = 'This is an important message.'
            context = {
                'name': name.upper(),
                'comment': comment,
                'webcast_title': webcast_title.upper()
            }
            message = get_template('eventsdisplay/support_email_template.html')
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(message.render(context), 'text/html')
            msg.send()
            return HttpResponse('You have successfully submitted a support request, we will be in touch shortly')