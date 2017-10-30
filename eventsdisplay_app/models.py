# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from eventsmanager_app.models import Webcast
from django.db import models

class Feedback(models.Model):
    webcast = models.ForeignKey(Webcast,on_delete=models.CASCADE,to_field='id')
    comment = models.TextField()
    name = models.CharField(max_length=100,default=None,null=False)
    surname = models.CharField(max_length=100,null=False,default=None)
    email= models.EmailField(default=None,null=False)
    def __unicode__(self):
        data = self.webcast
        return data

class Support(models.Model):
    webcast = models.ForeignKey(Webcast, on_delete=models.CASCADE, to_field='id')
    support_request = models.TextField()
    name = models.CharField(max_length=100, default=None, null=False)
    surname = models.CharField(max_length=100, null=False, default=None)
    email = models.EmailField(default=None, null=False)