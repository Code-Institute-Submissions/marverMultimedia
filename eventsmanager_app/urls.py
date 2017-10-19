from django.conf.urls import include,url
from eventsmanager_app import views

urlpatterns = [

        url(r'^$', views.eventsmanager, name='events_manager'),
        url(r'^eventcreation/$', views.eventCreation,name='event_creation'),
        url(r'^s3direct/',include('s3direct.urls')),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
]