# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponse
from django.db import connection,IntegrityError,DatabaseError,DataError
from django.views.generic import UpdateView,DeleteView,View,TemplateView,DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
import boto3
from django.contrib import messages, auth
from django.template.context_processors import csrf
from django.core import serializers
import datetime
import json
import stripe
import arrow
import re
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from marverProject.config import STRIPE_PUBLISHABLE,STRIPE_SECRET,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

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
                        return redirect('/eventsmanager/customer_%s' % user.id)
                    else:
                        messages.error(request, "Unable to log you in at this time!")
                else:
                    messages.error(request,"We were unable to take your payment with that card")
            except stripe.error.CardError:
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

            subscription_active = User.objects.get(email=request.POST.get('email'))


            user = auth.authenticate(email=request.POST.get('email'),
                                     password = request.POST.get('password'))
            print (subscription_active.subscription_end)
            if user is not None:
                if subscription_active.subscription_end > arrow.now():
                    auth.login(request,user)
                    messages.success(request,"You have Successfully Logged In")
                    return redirect('/eventsmanager/customer_%s' % user.id)
                else:
                    form.add_error(None, "Your Subscription has ended, please contact Support")
            else:
                form.add_error(None,"Your Details were not recognised! Please register")
    else:
        form = UserLoginForm()
    args = {'form':form}
    args.update(csrf(request))
    return render(request, 'eventsmanager_app/login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')

@login_required(login_url='/login/')
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
    except stripe.InvalidRequestError:
        messages.error(request,"Sorry there has been an error, please try again")
    return redirect('/eventsmanager/manage_subscription/customer_%s' % request.user.id)

@login_required(login_url='/login/')
def reactivate_subscription(request,pk):
    try:
        customer = User.objects.get(pk=pk)

        customer_sub = stripe.Customer.retrieve(
            customer.stripe_id
        )

        subscription = stripe.Subscription.retrieve(
            customer_sub.subscriptions.data[0].id
        )
        print(subscription)
        item_id = subscription['items']['data'][0].id
        plan= subscription['items']['data'][0]

        stripe.Subscription.modify(customer_sub.subscriptions.data[0].id,
                            items=[{
                                "id": item_id,
                                "plan" : "REG_MONTHLY"
                            }]
                                    )

        return HttpResponseRedirect('/eventsmanager/manage_subscription/customer_%s' % pk)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/eventsmanager/manage_subscription/customer_%s' % pk)




@method_decorator(login_required(login_url='/login/'),name='dispatch')
class ManageSubscription(DetailView):

    template_name = 'eventsmanager_app/manage_subscription.html'

    model=User

    def get_context_data(self, **kwargs):
        customer = User.objects.get(pk=self.kwargs['pk'])
        customer= stripe.Customer.retrieve(
            customer.stripe_id
        )
        subscription_details = customer.subscriptions.data[0]
        amount = customer.subscriptions.data[0].plan.amount / 100
        subscription_status = customer.subscriptions.data[0].cancel_at_period_end
        context = super(ManageSubscription, self).get_context_data(**kwargs)
        context['subscription_status'] = subscription_status
        context['subscription_details'] = subscription_details
        context['amount'] = amount

        return context


@csrf_exempt
def invoice_paid_webhook(request):
    event_json = json.loads(request.body)
    try:
        #event = stripe.Event.retrieve(event_json['object']['id'])
        cust= event_json['object']['customer']
        paid = event_json['object']['paid']
        user = User.objects.get(stripe_id=cust)
        if user and paid:
            user.subscription_end = arrow.now().replace(weeks=+4).datetime
            user.save()
    except stripe.InvalidRequestError:
        return HttpResponse(status=404)
    return HttpResponse(status=200)



@login_required(login_url='login/')
def eventsmanager(request,pk):
    webcast_list = Webcast.objects.all().filter(user_id=pk)
    user_id=pk
    current_url = request.build_absolute_uri()
    edit_url = current_url.replace('/eventsmanager/customer_%s/'% pk, '')
    return render(request, 'eventsmanager_app/events_manager.html', {'webcasts': webcast_list, 'current_url':edit_url,'user_id':user_id})

@login_required(login_url='login/')
def eventCreation(request):

    if request.method == 'POST':
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/eventsmanager/customer_%s' % form.cleaned_data['user_id'])
    else:
        form = EventCreation()

    return render(request, 'eventsmanager_app/event_creation.html', {'form': form})

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
        return '/eventsmanager/customer_%s/'% self.request.user.id

class DeleteEvent(DeleteView):
    model = Webcast
    template_name =  'eventsmanager_app/event_deletion.html'

    def get_success_url(self):
        return '/eventsmanager/customer_%s/' % self.request.user.id

def updatespeaker(request):
    if request.method == 'POST':
        speakers_id = request.POST['speakers_id']
        webcast_id = request.POST['webcast_id']
    try:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO marver.eventsmanager_app_webcast_speaker_id (webcast_id, speakers_id) VALUES  (%s , %s)""", [webcast_id,speakers_id])
            return HttpResponse('Speakers list updated successfully!')
    except:
            return HttpResponse('There have been an error processing the request, please try again')

def deletespeaker(request):
    if request.method == 'POST':
        speakers_id = request.POST['speakers_id']
        webcast_id = request.POST['webcast_id']

        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM marver.eventsmanager_app_webcast_speaker_id WHERE webcast_id = %s AND speakers_id = %s""",  [webcast_id,speakers_id])
            return HttpResponse('The Speaker/s have been successfully removed from this event')


def speakerCreation(request):
    if request.method == "POST":
            user_form1 = SpeakerCreation(request.POST, request.FILES)
            if user_form1.is_valid():
                response = HttpResponse('Speakers list updated successfully!', content_type="text/plain")
                user_form1.save()
                response.status_code = 200
                return response
            else:
                response = HttpResponse('An Error has occurred,please try again',content_type="text/plain")
                response.status_code = 500
                return response

def agendaView(request) :

    if request.method == 'POST':
        agenda_array = request.POST['agenda']
        webcast_id = request.POST['webcast_id']
        agenda_id = request.POST['agenda_id']
        if agenda_id == "0":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""INSERT INTO marver.eventsmanager_app_agenda (agenda,webcast_id_id) VALUES (%s , %s)""",[agenda_array,webcast_id])
                return HttpResponse('The Agenda have been successfully added to this event')
            except:
                return HttpResponse('There has been a problem creating the agenda, please try again')
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                    "UPDATE marver.eventsmanager_app_agenda SET agenda = (%s) WHERE id = %s ",[agenda_array,agenda_id])
                return HttpResponse('The Agenda have been successfully updated')
            except:
                return HttpResponse('There has been a problem with updating, please try again')

def assetCreation(request):
    if request.method == "POST":
        user_form1 = AssetCreation(request.POST, request.FILES)
        if user_form1.is_valid():
                user_form1.save()
                response = HttpResponse('The Document has been uploaded successfully', content_type="text/plain")
                response.status_code = 200
                return response
        else:
                response = HttpResponse('Some Data in the form are in valid,please check and try again', content_type="text/plain")
                response.status_code = 500
                return response



def assetAddition(request):
    if request.method == 'POST':
        assets_id = request.POST['assets_id']
        webcast_id = request.POST['webcast_id']
    try:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO marver.eventsmanager_app_webcast_webcast_asset_ID (webcast_id, assets_id) VALUES  (%s , %s)""", [webcast_id,assets_id])
        return HttpResponse('The Asset/s have been successfully added to this event')
    except IntegrityError:
        response = HttpResponse('There has been a problem, please try again', content_type="text/plain")
        response.status_code = 500
        return response

def assetDeletion(request):
    if request.method == 'POST':
        assets_id = request.POST['assets_id']
        webcast_id = request.POST['webcast_id']
    try:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM marver.eventsmanager_app_webcast_webcast_asset_ID WHERE webcast_id = %s AND assets_id = %s""",[webcast_id,assets_id])
            return HttpResponse('Asset/s has been successfully removed from this event')

    except IntegrityError:
            response = HttpResponse('There has been a problem, please try again',content_type="text/plain")
            response.status_code = 500
            return response

@csrf_exempt
def thumbnail_upload(request):
    if request.method == 'POST':
        datauri = request.POST.get('webcast_image','')
        webcast_id = request.POST.get('webcast_id','')
        path = 'https://elasticbeanstalk-eu-west-2-932524864295.s3.amazonaws.com/media/webcast_'+ webcast_id +'/Thumbnail.png'
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE marver.eventsmanager_app_webcast SET webcast_img = (%s) WHERE id = %s ",
                [path, webcast_id])
        imgstr = re.search(r'base64,(.*)',datauri).group(1)
        output = open('output.png','wb')
        output.write(imgstr.decode('base64'))
        output.close()
        data = open('output.png','rb')
        s3 = boto3.resource('s3',aws_access_key_id= AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3.Bucket('elasticbeanstalk-eu-west-2-932524864295').put_object(Key='media/webcast_'+ webcast_id + "/Thumbnail.png",Body=data)
        return HttpResponse('Your Thumbnail Has been Successfully Set')