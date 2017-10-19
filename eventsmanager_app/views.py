# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
import boto3
from django.contrib import messages, auth
from django.template.context_processors import csrf
import datetime
import stripe
import arrow
from marverProject.config import STRIPE_PUBLISHABLE,STRIPE_SECRET

stripe.api_key = STRIPE_SECRET

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Customer.create(
                    email=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id'],
                    plan='REG_MONTHLY'
                )
                if customer:
                    user = form.save()
                    user.stripe_id = customer.id
                    user.subscription_end = arrow.now().replace(weeks=+4).datetime
                    user.save()
                    user = auth.authenticate(email=request.POST.get('email'),
                                         password=request.POST.get('password1'))
                    if user:
                        auth.login(request,user)
                        messages.success(request, "You have Successfully registered")
                        return redirect('events_manager')
                    else:
                        messages.error(request, "Unable to log you in at this time!")
                else:
                    messages.error(request,"We were unable to take your payment with that card")
            except stripe.error.CardError, e:
                messages.error(request,"Your card was declined!")
    else:
        today =datetime.date.today()
        form = UserRegistrationForm()

    args = {'form': form, 'publishable':STRIPE_PUBLISHABLE}
    args.update(csrf(request))
    return render(request, 'eventsmanager_app/register.html', args)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():

            user = auth.authenticate(email=request.POST.get('email'),
                                     password = request.POST.get('password'))
            if user is not None:
                auth.login(request,user)
                messages.success(request,"You have Successfully Logged In")
                return redirect('events_manager')
            else:
                form.add_error(None,"Your Details were not recognised! Please contact the administrator to request access")
    else:
        form = UserLoginForm()
    args = {'form':form}
    args.update(csrf(request))
    return render(request, 'eventsmanager_app/login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')

@login_required(login_url='login/')
def eventsmanager(request):
    webcast_list = Webcast.objects.all()
    current_url = request.build_absolute_uri()
    edit_url = current_url.replace('/events_manager/', '')
    return render(request, 'eventsmanager_app/events_manager.html', {'webcasts': webcast_list, 'current_url':edit_url})

@login_required(login_url='login/')
def eventCreation(request):

    if request.method == 'POST':
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/events_manager/')
    else:
        form = EventCreation()
    webcast_speakers = Speakers.objects.all()

    return render(request, 'eventsmanager_app/event_creation.html', {'form': form, 'speakers':webcast_speakers})

