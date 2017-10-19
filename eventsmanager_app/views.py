# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.generic import UpdateView,DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
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
    edit_url = current_url.replace('/eventsmanager/', '')
    return render(request, 'eventsmanager_app/events_manager.html', {'webcasts': webcast_list, 'current_url':edit_url})

@login_required(login_url='login/')
def eventCreation(request):

    if request.method == 'POST':
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/eventsmanager/')
    else:
        form = EventCreation()

    return render(request, 'eventsmanager_app/event_creation.html', {'form': form})

@login_required(login_url='/login/')
def administration(request):
    webcast_list = Webcast.objects.all()
    current_url = request.build_absolute_uri()
    edit_url = current_url.replace('/administration/', '')
    return render(request,'eventsmanager_app/events_manager.html',{'webcasts': webcast_list,'current_url':edit_url})

@login_required(login_url='/login/')
def webcastCreation(request):

    if request.method == 'POST':
        form = WebcastCreation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/administration/')
    else:
        form = WebcastCreation()
    webcast_speakers = Speakers.objects.all()

    return render(request, 'eventsmanager_app/event_creation.html', {'form': form, 'speakers':webcast_speakers})

@method_decorator(login_required(login_url='/login/'),name='dispatch')
class UpdateEvent(UpdateView):

    model = Webcast
    template_name = 'eventsmanager_app/event_edit.html'
    form_class = WebcastEditForm

    def get_context_data(self, **kwargs):
        saveThumbnail = ThumbnailsUpload(self.request.GET or None)
        assetCreationForm = AssetCreation(self.request.GET or None)
        speakerCreationForm = SpeakerCreation(self.request.GET or None)
        uploadVideo=S3DirectUploadForm(self.request.GET or None)
        context = super(UpdateEvent, self).get_context_data(**kwargs)
        context['thumbnailUploadForm'] = saveThumbnail
        context['videoUpload'] = uploadVideo
        context['speakers'] = Speakers.objects.all().filter(webcast__id__contains = self.kwargs['pk'])
        context['all_speakers'] = Speakers.objects.all().exclude(webcast__id__contains = self.kwargs['pk'] )
        context['webcast']= get_object_or_404(Webcast, pk=self.kwargs['pk'])
        context['speakerForm'] = speakerCreationForm
        context['assetsForm'] = assetCreationForm
        context['all_assets'] = Assets.objects.all().exclude(webcast__id__contains = self.kwargs['pk'] )
        try:
            agenda_id = Agenda.objects.get(webcast_id=self.kwargs['pk'])
            agenda_id_edit = agenda_id.agenda
            context['agenda_id'] = agenda_id.id
            context['agenda'] = agenda_id_edit
        except ObjectDoesNotExist:
            context['agenda_id'] = "0"
        try:
            assets_id = Assets.objects.all().filter(webcast__id__contains = self.kwargs['pk'])
            context['assets'] = assets_id
        except ObjectDoesNotExist:
            context['assets'] = None
        return context

    def get_success_url(self):
        return reverse('events_manager')

class DeleteEvent(DeleteView):
    model = Webcast
    template_name =  'eventsmanager_app/event_deletion.html'

    def get_success_url(self):
        return reverse('events_manager')