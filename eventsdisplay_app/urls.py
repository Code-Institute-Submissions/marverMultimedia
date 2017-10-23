from django.conf.urls import include,url
from eventsdisplay_app import views

urlpatterns = [

        url(r'^$', views.eventslibrary),
        url(r'^player/event_(?P<id>\d+)/*', views.event_player,name='player'),
        url(r'^comment/', views.event_comment,name='comment'),

]