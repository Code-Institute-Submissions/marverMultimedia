from django.conf.urls import include,url
from eventsdisplay_app import views

urlpatterns = [

        url(r'^$', views.eventslibrary),
        url(r'^player/event_(?P<id>\d+)/$', views.event_player,name='player'),
        url(r'^comment/', views.event_comment,name='comment'),
        url(r'^eventrating/', views.event_rating,name='rating'),
        url(r'^orderevents/option_(?P<option>[0-9A-Za-z_]+)/$', views.events_order,name='events_order'),
        url(r'^searchevents/search_(?P<search>[0-9A-Za-z_]+)/$', views.search_events,name='events_search'),


]