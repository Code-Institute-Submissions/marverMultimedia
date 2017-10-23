# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase,TestCase,TransactionTestCase
from eventsdisplay_app.views import home_page,eventslibrary,event_player
from django.core.urlresolvers import resolve
from eventsmanager_app.models import Webcast,Customers,Speakers,Agenda,Assets

class EventDisplayAppTest(SimpleTestCase):
    def test_home_page(self):
        home_page_test = resolve('/')
        self.assertEqual(home_page_test.func,home_page)

    def test_events_library(self):
        events_library_test = resolve('/events/')
        self.assertEqual(events_library_test.func,eventslibrary)

    def test_event_player(self):
        events_player_test = resolve('/events/player/event_1')
        self.assertEqual(events_player_test.func,event_player)

class EventDisplayStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.customer = Customers.objects.create(
            id = 1,
            company_name = 'test',
            company_address = 'test drive',
            company_type = 'digital',
            main_contact_name = 'luca',
            main_contact_surname = 'licata',
            main_contact_email = 'lucalicata@hotmail.com',
            customer_status = 'active'

        )

        cls.webcast = Webcast.objects.create(
            id = 1,
            customer_id_id= 1,
            user_id=1,
            creation_date = '2017-10-20',
            webcast_status = 'ON_DEMAND',
            webcast_title = 'test',
            webcast_date = '2017-11-20',
            webcast_time = '15:30',
            webcast_asset_ID = '',
            webcast_img ='',
            speaker_id = '',
            webcast_description = '',
            webcast_video = ''
        )

    def test_home_page_status(self):
        home_page_test = self.client.get('/')
        self.assertEqual(home_page_test.status_code,200)

    def test_eventslibrary_status(self):
        events_library_test = self.client.get('/events/')
        self.assertEqual(events_library_test.status_code,200)

    def test_event_player_status(self):
        events_player_test = self.client.get('/events/player/event_1/test')
        self.assertEqual(events_player_test.status_code,200)

class ContextDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = Customers.objects.create(
            id=1,
            company_name='test',
            company_address='test drive',
            company_type='digital',
            main_contact_name='luca',
            main_contact_surname='licata',
            main_contact_email='lucalicata@example.com',
            customer_status='active'

        )

        cls.webcast_future = Webcast.objects.create(
            id=1,
            customer_id_id=1,
            user_id = 1,
            creation_date='2017-10-20',
            webcast_status='ON_DEMAND',
            webcast_title='test',
            webcast_date='2017-11-20',
            webcast_time='15:30',
            webcast_asset_ID='',
            webcast_img='',
            speaker_id='',
            webcast_description='',
            webcast_video='',
        )

        cls.webcast_archived = Webcast.objects.create(
            id=2,
            customer_id_id=1,
            user_id=1,
            creation_date='2017-05-20',
            webcast_status='ON_DEMAND',
            webcast_title='test_archived',
            webcast_date='2017-08-20',
            webcast_time='15:30',
            webcast_asset_ID='',
            webcast_img='',
            speaker_id='',
            webcast_description='',
            webcast_video='',

        )

        cls.speakers = Speakers.objects.create(
            id = 1,
            speaker_name = 'Luca',
            speaker_surname = 'Licata',
            speaker_email = 'lucalicata@example.com',
            speaker_title = 'Director',
            speaker_bio = '',
            speaker_pic_url = ''
        )

        cls.agenda = Agenda.objects.create(
            id =1,
            agenda = ['agenda-point-1','agenda-point-2'],
            webcast_id_id = 1
        )

        cls.assets = Assets.objects.create(
            id = 1,
            asset_type = 'Document',
            asset_upload = '',
            asset_name = 'test'
        )



    def test_home_page_context_data(self):
        home_page_test = self.client.get('/')
        self.assertEqual(home_page_test.context['webcasts'][0].webcast_title,'test')
        self.assertEqual(len(home_page_test.context['webcasts']),1)
        self.assertEqual(len(home_page_test.context['archived_webcasts']),1)


    def test_events_library_context_data(self):
        events_library_test = self.client.get('/events/')
        self.assertEqual(len(events_library_test.context['events']),2)

    def test_events_player_context_data(self):
        comment = {
            'name': 'Luca',
            'surname': 'Licata',
            'email': 'lucalicata81@example.com',
            'comment': 'test',
            'webcast_id': 1,
            'webcast_title':'test'
        }
        events_player_test = self.client.get('/events/player/event_1/test')
        events_player_feedback_test = self.client.post('/events/comment/',comment)
        self.assertEqual(len(events_player_test.context['webcasts']),1)
        self.assertEqual(events_player_test.context['event_id'].webcast_title,'test')
        self.assertEqual(events_player_test.context['agenda'].agenda,['agenda-point-1','agenda-point-2'])
        self.assertEqual(events_player_feedback_test.content,'success')