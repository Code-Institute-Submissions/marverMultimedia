# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_mysql.models import Model , JSONField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from s3direct.fields import S3DirectField


def webcast_imagege_path(instance,filename):
    return 'media/webcast_{0}/{1}'.format(instance.id,filename)

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
    creation_date = models.DateTimeField(auto_now_add=True)
    webcast_status = models.CharField(max_length=30,default=None, choices=(('OD','ON-DEMAND'),('LIVE','LIVE')),verbose_name='Webcast Type')
    webcast_title = models.CharField(max_length=150,default=None)
    webcast_date = models.DateField(default=None)
    webcast_time = models.TimeField(default=None)
    webcast_asset_ID = models.ManyToManyField(Assets,verbose_name='Select Assets',blank=True)
    webcast_img = models.ImageField(upload_to=webcast_imagege_path,default='marverhigres.png',verbose_name='Upload Main Image',blank=True)
    speaker_id = models.ManyToManyField(Speakers,verbose_name='Speakers Creation/Selection ',blank=True)
    webcast_description = models.TextField(blank=True)
    webcast_video = S3DirectField(dest='example_destination', verbose_name='On-Demand Video Upload', blank=True)


    def __unicode__(self):
        return self.webcast_title

    def __str__(self):
        return self.webcast_title

    def get_absolute_url(self):
        return "/webcasts/player/webcast_%s/%s" %(self.id,self.webcast_title)


    def get_absolute_url_edit(self):
        return reverse("/administration/webcast_edit/webcast_%s" %(self.id), kwargs={'pk':self.pk})

class Agenda(models.Model):
    agenda= JSONField()
    webcast_id = models.ForeignKey(Webcast,on_delete=models.CASCADE,to_field='id', default=None)


class Feedback(models.Model):
    webcast = models.ForeignKey(Webcast,on_delete=models.CASCADE,to_field='id')
    comment = models.TextField()
    name = models.CharField(max_length=100,default=None,null=False)
    surname = models.CharField(max_length=100,null=False,default=None)
    email= models.EmailField(default=None,null=False)
    def __unicode__(self):
        data = self.webcast
        return data


class Thumbnails(models.Model):
    webcast_image = models.ImageField(upload_to=webcast_imagege_path, default='marverhigres.png',
                                    verbose_name='Upload Main Image', blank=True)
    webcast_id = models.ForeignKey(Webcast, on_delete=models.CASCADE, to_field='id', default=None)
