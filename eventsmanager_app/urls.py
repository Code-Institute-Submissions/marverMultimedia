from django.conf.urls import include,url
from eventsmanager_app import views

urlpatterns = [

        url(r'^$', views.eventsmanager),
        url(r'^eventcreation/$', views.eventCreation,name='event_creation'),
        url(r'^s3direct/',include('s3direct.urls')),

]