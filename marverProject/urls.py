
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
    url(r'^orderevents/$', eventsmanager_views.events_order_manager, name='events_order_manager'),
    url(r'^searchevents/$', eventsmanager_views.search_events_manager, name='events_search_manager'),
]
