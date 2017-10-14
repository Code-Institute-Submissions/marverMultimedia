from django.conf.urls import include,url
from eventmanager_app import views

urlpatterns = [

        url(r'^$', views.eventsmanager),
]