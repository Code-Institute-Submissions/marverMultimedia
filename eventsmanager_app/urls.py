from django.conf.urls import include,url
from django.conf import settings
from eventsmanager_app import views

urlpatterns = [

        url(r'^customer_(?P<pk>\d+)/$', views.eventsmanager, name='event_manager'),
        url(r'^eventcreation/$', views.eventCreation,name='event_creation'),
        url(r'^eventupdate/event_(?P<pk>\d+)/$', views.UpdateEvent.as_view(), name='event_edit'),
        url(r'^event_deletion/event_(?P<pk>\d+)/$', views.DeleteEvent.as_view(), name='event_deletion'),
        url(r'^speakers_addition',views.updatespeaker),
        url(r'^speakers_deletion',views.deletespeaker),
        url(r'^speakers_creation',views.speakerCreation),
        url(r'^asset_creation', views.assetCreation),
        url(r'^assets_addition', views.assetAddition),
        url(r'^assets_deletion', views.assetDeletion),
        url(r'^s3direct/',include('s3direct.urls')),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
        url(r'^manage_subscription/customer_(?P<pk>\d+)/$', views.ManageSubscription.as_view(),name='managesubscription'),
        url(r'^cancel_subscription/$', views.cancel_subscription,name='cancelsubscription'),
        url(r'^reactivate_subscription/(?P<pk>\d+)/$', views.reactivate_subscription,name='reactivatesubscription'),
        url(r'^invoice_paid/$', views.invoice_paid_webhook,name='invoicepaidwebhook'),

]