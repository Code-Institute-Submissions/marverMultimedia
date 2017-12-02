"""marverProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from eventsdisplay_app import views
from eventsmanager_app import views as eventsmanager_views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_page),
    url(r'^eventsmanager/', include('eventsmanager_app.urls')),
    url(r'^events/', include('eventsdisplay_app.urls')),
    url(r'^agenda', eventsmanager_views.agendaView),
    url(r'^chapters', eventsmanager_views.chaptersView),
    url(r'^thumbnail_upload',eventsmanager_views.thumbnail_upload),
    url(r'^increase_siteattendance/',eventsmanager_views.increase_site_visits, name='increase_site_visits'),
    url(r'^increase_eventattendance/',eventsmanager_views.increase_event_visits, name='increase_event_visits'),

]
