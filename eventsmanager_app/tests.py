# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import SimpleTestCase,TestCase,TransactionTestCase
from eventsmanager_app.views import register
from django.core.urlresolvers import resolve
from eventsmanager_app.models import Webcast,Customers,Speakers,Agenda,Assets,User
from django.contrib.auth.models import UserManager
import simplejson as json
from io import BytesIO
class LoginRegistrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='lucalicata@hotmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_registration(self):
        data = {
            'username' : 'lucalicata@example.co.uk',
            'password' : 'lemon64',
            'stripe_id' : 'cus_',
        }

        test_registration_post = self.client.post('/eventsmanager/register/',data)
        self.assertEqual(test_registration_post.status_code,200)
        test_registration_get = self.client.get('/eventsmanager/register/')
        self.assertContains(test_registration_get,'publishable')
        self.assertContains(test_registration_get,'form')

    def test_login(self):

        test_login = self.client.login(email='lucalicata@hotmail.com',password='12345')
        self.assertTrue(test_login)

class EventManagerTests(TestCase):
    data = {
        'user_id': 1,
        'customer_id': 1,
        'webcast_status': 'ON-DEMAND',
        'webcast_title': 'test',
        'webast_date': '30-11-2017',
        'webcast_time': '15:30'
    }

    def setUp(self):
        self.user = User.objects.create(email='lucalicata@hotmail.com')
        self.user.set_password('12345')
        self.user.save()

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
        cls.webcast = Webcast.objects.create(
            id=1,
            customer_id_id=1,
            user_id=1,
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
            id=1,
            speaker_name='Luca',
            speaker_surname='Licata',
            speaker_email='lucalicata@example.com',
            speaker_title='Director',
            speaker_bio='',
            speaker_pic_url=''
        )

        cls.agenda = Agenda.objects.create(
            id=1,
            agenda=['agenda-point-1', 'agenda-point-2'],
            webcast_id_id=1
        )

        cls.assets = Assets.objects.create(
            id=1,
            asset_type='Document',
            asset_upload='',
            asset_name='test'
        )

    def test_eventsmanager_view(self):
        self.client.login(email='lucalicata@hotmail.com', password='12345')
        event_manager_view=self.client.get('/eventsmanager/customer_1/')
        self.assertEqual(event_manager_view.status_code,200)
        self.assertEqual(event_manager_view.context['webcasts'][0].webcast_title,'test')
        self.assertEqual(event_manager_view.context['webcasts'][1].webcast_title,'test_archived')
        self.assertEqual(event_manager_view.context['user_id'],'1')

    def test_event_creation_view(self):

        self.client.login(email='lucalicata@hotmail.com', password='12345')
        event_creation = self.client.post('/eventsmanager/eventcreation/', self.data,follow=True)
        self.assertRedirects(event_creation,'/eventsmanager/customer_1/',status_code=302,target_status_code=200)

    def test_event_edit_view(self):
        self.client.login(email='lucalicata@hotmail.com', password='12345')
        event_edit = self.client.post('/eventsmanager/eventupdate/event_1/',self.data)
        self.assertEqual(event_edit.context['webcast'].webcast_title,'test')
        self.assertEqual(event_edit.context['all_speakers'][0].speaker_name,'Luca')
        self.assertEqual(event_edit.context['all_assets'][0].asset_name,'test')
        self.assertEqual(event_edit.context['agenda'][0],'agenda-point-1')
        self.assertEqual(event_edit.status_code,200)


    def test_update_speaker_view(self):
        speaker_update = self.client.post('/eventsmanager/speakers_addition/',data={'speakers_id' : 1 , 'webcast_id':1})
        self.assertEqual(speaker_update.status_code,200)
        self.assertEqual(speaker_update.content,'Speakers list updated successfully!')
        speaker_update_fail = self.client.post('/eventsmanager/speakers_addition/', data={'speakers_id': 0, 'webcast_id': 0})
        self.assertEqual(speaker_update_fail.content, 'There have been an error processing the request, please try again')

    def test_delete_speaker_view(self):
        speaker_delete = self.client.post('/eventsmanager/speakers_deletion/', data={'speakers_id': 1, 'webcast_id': 1})
        self.assertEqual(speaker_delete.status_code, 200)
        self.assertEqual(speaker_delete.content, 'The Speaker/s have been successfully removed from this event')

    def test_speaker_creation(self):
        speaker_create = self.client.post('/eventsmanager/speakers_creation/',data={
            'id' : 1,
            'speakers_id':1,
            'webcast_id':1,
            'speaker_name' : 'Luca',
            'speaker_surname' : 'Licata',
            'speaker_email' : 'lucalicata@example.com',
            'speaker_title' : 'Director',
            'speaker_bio' : '',
            'speaker_pic_url' : ''
        })
        self.assertEqual(speaker_create.status_code,200)
        self.assertEqual(speaker_create.content,'Speakers list updated successfully!')
        speaker_create_fail = self.client.post('/eventsmanager/speakers_creation/', data={
            'id': 1,
            'speakers_id': 1,
            'webcast_id': 0,
            'speaker_name': 'Luca',
            'speaker_surname': 'Licata',
            'speaker_email': '',
            'speaker_title': '',
            'speaker_bio': '',
            'speaker_pic_url': ''
        })
        self.assertEqual(speaker_create_fail.status_code, 500)
        self.assertEqual(speaker_create_fail.content, 'An Error has occurred,please try again')

    def test_agenda_view(self):
        agenda = json.dumps(['agenda-point-1','agenda-point-2'],indent='\t')
        agenda_test = self.client.post('/agenda/',data={
            'agenda' : agenda,
            'webcast_id': 1,
            'agenda_id' : 1
        })
        self.assertEqual(agenda_test.status_code,200)
        self.assertEqual(agenda_test.content,'The Agenda have been successfully updated')
        agenda_test_fail = self.client.post('/agenda/', data={
            'agenda': ['agenda-point-1', 'agenda-point-2'],
            'webcast_id': 1,
            'agenda_id': 1
        })
        self.assertEqual(agenda_test_fail.status_code, 200)
        self.assertEqual(agenda_test_fail.content, 'There has been a problem with updating, please try again')
        agenda_test_create = self.client.post('/agenda/', data={
            'agenda': agenda,
            'webcast_id': 1,
            'agenda_id': 0
        })
        self.assertEqual(agenda_test_create.status_code, 200)
        self.assertEqual(agenda_test_create.content, 'The Agenda have been successfully added to this event')
        agenda_test_fail = self.client.post('/agenda/', data={
            'agenda': ['agenda-point-1', 'agenda-point-2'],
            'webcast_id': 1,
            'agenda_id': 0
        })
        self.assertEqual(agenda_test_fail.status_code, 200)
        self.assertEqual(agenda_test_fail.content, 'There has been a problem creating the agenda, please try again')

    def test_asset_creation(self):
        pdf = BytesIO(b'myDocument')
        pdf.name = 'webcast.pdf'
        asset_creation_test = self.client.post('/eventsmanager/asset_creation/',data={

            'asset_type': 'DOC',
            'asset_upload': pdf,
            'asset_name': 'test'
        })
        self.assertEqual(asset_creation_test.status_code,200)
        self.assertEqual(asset_creation_test.content,'The Document has been uploaded successfully')
        asset_creation_test_fail = self.client.post('/eventsmanager/asset_creation/', data={

            'asset_type': 'DOC',
            'asset_upload': pdf,
            'asset_name': ''
        })
        self.assertEqual(asset_creation_test_fail.status_code, 500)
        self.assertEqual(asset_creation_test_fail.content, 'Some Data in the form are in valid,please check and try again')

    def test_asset_addition(self):
        asset_addition_test = self.client.post('/eventsmanager/assets_addition/',data={
            'assets_id' : 1,
            'webcast_id' : 1
        })
        self.assertEqual(asset_addition_test.status_code,200)
        self.assertEqual(asset_addition_test.content,'The Asset/s have been successfully added to this event')
        asset_addition_test_fail = self.client.post('/eventsmanager/assets_addition/', data={
            'assets_id': 1,
            'webcast_id': 1
        })
        self.assertEqual(asset_addition_test_fail.status_code, 500)
        self.assertEqual(asset_addition_test_fail.content, 'There has been a problem, please try again')
        asset_addition_test_fail = self.client.post('/eventsmanager/assets_addition/', data={
            'assets_id': 2,
            'webcast_id': 3
        })
        self.assertEqual(asset_addition_test_fail.status_code, 500)
        self.assertEqual(asset_addition_test_fail.content, 'There has been a problem, please try again')

    def test_asset_deletion_view(self):
        asset_deletion_view = self.client.post('/eventsmanager/assets_deletion/', data={
            'assets_id' : 1,
            'webcast_id' : 1
        })
        self.assertEqual(asset_deletion_view.status_code,200)
        self.assertEqual(asset_deletion_view.content,'Asset/s has been successfully removed from this event')
        asset_deletion_test_fail = self.client.post('/eventsmanager/assets_addition/', data={
            'assets_id': 2,
            'webcast_id': 3
        })
        self.assertEqual(asset_deletion_test_fail.status_code,500)

    def test_thumbnail_upload(self):
        img = BytesIO(b'myImage')
        img.name = 'webcast.jpg'

        thumbnail_upload_test = self.client.post('/thumbnail_upload/',data={
            'webcast_id' : 1,
            'webcast_image' : img
        })

        self.assertEqual(thumbnail_upload_test.status_code,200)