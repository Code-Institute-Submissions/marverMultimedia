# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from eventsmanager_app.models import *
from eventsmanager_app.models import Feedback, Support, EventRating
import datetime
from django.views.decorators.csrf import csrf_exempt


def home_page(request):
    upcoming_webcasts = Webcast.objects.all().filter(webcast_date__gte=datetime.date.today())
    archived_webcasts = Webcast.objects.all().filter(webcast_date__lte=datetime.date.today())[:6]

    return render(request, "eventsdisplay/home.html", {'webcasts':upcoming_webcasts , 'archived_webcasts':archived_webcasts})


def eventslibrary(request):

    events_list = Webcast.objects.all().order_by('-webcast_date')
    request.build_absolute_uri()
    return render(request, "eventsdisplay/events.html", {'events' : events_list})

#view responsible for arranging events by month
@csrf_exempt
def events_order(request):

    option = request.GET.get('option')

    if 0 == int(option):
        events_list = Webcast.objects.all().order_by('webcast_date')
        return render(request,"eventsdisplay/events.html",{'events' : events_list})
    else:
        events_list = Webcast.objects.all().filter(webcast_date__month=int(option))
        if len(events_list) > 0:
            return render(request, "eventsdisplay/events.html", {'events': events_list})
        else:
            response = HttpResponse('OOOOps, it seems there were no events on the selected month',
                                    content_type="text/plain")
            response.status_code = 404
            return response

#Event Search Section
@csrf_exempt
def search_events(request):

    search = request.GET.get('search')

    events_list = Webcast.objects.raw("""SELECT * FROM marver.eventsmanager_app_webcast WHERE webcast_title LIKE concat('%%', %s, '%%'); """,[search])

    try:
        print(events_list[0])
        return render(request, "eventsdisplay/events.html",{'events' : events_list})
    except IndexError:
        response = HttpResponse('OOOOps, your search has not returned any results',
                                content_type="text/plain")
        response.status_code = 404
        return response


#Event Player Management

def event_player(request, id):
    event_id = get_object_or_404(Webcast, pk=id)
    event_list = Webcast.objects.all().filter(webcast_date__lte=datetime.date.today()).exclude(id__exact=id)
    single_assets_list = Assets.objects.all().filter(webcast__id__contains=id )
    speakers_list = Speakers.objects.all().filter(webcast__id__contains=id)
    try:
        agenda_list = Agenda.objects.get(webcast_id=id)
        print(agenda_list)
        agenda_id = agenda_list.id
    except:
        agenda_list = None
        agenda_id = 0

        print(agenda_id)

    try:
        chapter_list = get_object_or_404(Chapters, webcast_id=id)
    except:
        chapter_list = None

    return render(request, "eventsdisplay/player.html", {'webcasts':event_list, 'event_id':event_id, 'assets':single_assets_list, 'agenda':agenda_list, 'speakers_list':speakers_list , 'chapters_list':chapter_list,'agenda_id':agenda_id})


def event_comment(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        comment = request.POST['comment']
        webcast_id = request.POST['webcast_id']
        webcast_title = request.POST['webcast_title']
        date = request.POST['date']

        if request.POST['form'] == "commentForm":

            try:
                Feedback.objects.create(
                    name=name,
                    surname=surname,
                    email=email,
                    comment=comment,
                    webcast_id=webcast_id,
                    date=date,
                    event_title=webcast_title
                )

                subject, from_email, to = 'Thank you for contacting Marver', 'lucalicata@hotmail.com', email
                text_content = 'This is an important message.'
                context = {
                    'name': name.upper(),
                    'comment': comment,
                    'webcast_title': webcast_title.upper()
                }
                message = get_template('eventsdisplay/comment_email_template.html')
                msg = EmailMultiAlternatives(subject ,text_content, from_email, [to])
                msg.attach_alternative(message.render(context), 'text/html')
                msg.send()
                return HttpResponse('You have successfully submitted your feedback, thank you!!')
            except BadHeaderError:
                return HttpResponse('There have been an error please try again')
        else:
            issue_type = request.POST['issue_type']
            platform = request.POST['platform']
            device = request.POST['device']
            Support.objects.create(
                name=name,
                surname=surname,
                email=email,
                support_request=comment,
                webcast_id=webcast_id,
                issue_type=issue_type,
                date=date,
                platform=platform,
                device=device,
                event_title=webcast_title
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


@csrf_exempt
def event_rating(request):

        webcast_id = request.POST['webcast_id']
        rating = request.POST['rating']
        event_title = request.POST['event_title']
        try:
            EventRating.objects.create(

                webcast_id=webcast_id,
                rating=rating,
                event_title=event_title
            )
            return HttpResponse('Thank you!!')
        except Exception:
            return HttpResponse('There has been an error, please try again')
