# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_mysql.models import JSONField
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from s3direct.fields import S3DirectField


def webcast_image_path(instance,filename):
    return 'media/webcast_{0}/{1}'.format(instance.id,filename)

class AccountUserManager(UserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser,**extra_fields):
        now=timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,is_staff=is_staff,is_active=True,
                          is_superuser=is_superuser,date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

class User(AbstractUser):
    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now)
    objects=AccountUserManager()

    def get_absolute_url(self):
        return "/eventsmanager/manage_subscription/customer_%s" %(self.id)


class Customers(models.Model):
    company_name = models.CharField(max_length=30,default=None)
    company_address = models.CharField(max_length=150,default=None)
    company_type = models.CharField(max_length=30,default=None)
    main_contact_name = models.CharField(max_length=30,default=None)
    main_contact_surname = models.CharField(max_length=30,default=None)
    main_contact_email = models.CharField(max_length=60,default=None)
    customer_status = models.CharField(max_length=20,default=None)

    def __unicode__(self):
        data = self.company_name
        return data
    def __str__(self):
        data = self.company_name
        return data


class Speakers(models.Model):
        speaker_name = models.CharField(max_length=30,default=None)
        speaker_surname = models.CharField(max_length=30,default=None)
        speaker_email = models.CharField(max_length=60,default=None)
        speaker_title = models.CharField(max_length=60,default=None)
        speaker_bio = models.CharField(max_length=60,default=None,blank=True)
        speaker_pic_url = models.ImageField(upload_to='speakers', default=None, verbose_name='Upload Main Image',blank=True)

        def __unicode__(self):
            data = self.speaker_name + "" + self.speaker_surname
            return data
        def __str__(self):
            data = self.speaker_name + "" + self.speaker_surname
            return data


class Assets(models.Model):
    asset_types = (('DOC','Document'),('PPT','Presentation'))
    asset_upload = models.FileField(upload_to='assets')
    asset_name = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=30,choices=asset_types)

    def __unicode__(self):
        data = self.asset_name
        return data
    def __str__(self):
        data = self.asset_name
        return data

class Webcast(models.Model):
    customer_id = models.ForeignKey(Customers, default=None, on_delete=models.CASCADE)
    user_id = models.IntegerField(default=None)
    creation_date = models.DateTimeField(auto_now_add=True)
    webcast_status = models.CharField(max_length=30,default=None, choices=(('OD','ON-DEMAND'),('LIVE','LIVE')),verbose_name='Webcast Type')
    webcast_title = models.CharField(max_length=150,default=None)
    webcast_date = models.DateField(default=None)
    webcast_time = models.TimeField(default=None)
    webcast_asset_ID = models.ManyToManyField(Assets,verbose_name='Select Assets',blank=True)
    webcast_img = models.ImageField(upload_to='media/',default='marverhigres.png',verbose_name='Upload Main Image',blank=True)
    speaker_id = models.ManyToManyField(Speakers,verbose_name='Speakers Creation/Selection ',blank=True)
    webcast_description = models.TextField(blank=True)
    webcast_video = S3DirectField(dest='example_destination', verbose_name='On-Demand Video Upload', blank=True)


    def __unicode__(self):
        return self.webcast_title

    def __str__(self):
        return self.webcast_title

    def get_absolute_url(self):
        return "/events/player/event_%s/" %(self.id)


class Agenda(models.Model):
    agenda= JSONField()
    webcast_id = models.ForeignKey(Webcast,on_delete=models.CASCADE,to_field='id', default=None)

