# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse

from django.contrib import admin
from .models import Webcast
from .models import Customers
from .models import Speakers
from .models import Assets
from .models import Agenda


class EventAdmin(admin.ModelAdmin):

    list_filter = ('webcast_date',)

    filter_horizontal = ('webcast_asset_ID','speaker_id')

    list_display = ('webcast_title','webcast_date')

    ordering = ('webcast_date',)

    save_as = True
    search_fields = ['webcast_title']

    def view_on_site(self, Webcast):
        url = reverse('player', kwargs={'id' : Webcast.id })
        return '' + url

    pass

admin.site.register(Webcast,EventAdmin)
admin.site.register(Customers)
admin.site.register(Speakers)
admin.site.register(Assets)
admin.site.register(Agenda)