from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service, Paperwork, Paperwork_Service_User
import json
from django.db.utils import IntegrityError

class GetListofPaperWorkTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_fake_service_return_empty_list(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 999
        response = self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), 0)
        

    def test_anonymous_user_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        service_id = 1
        with self.assertRaises(TypeError): 
            self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
       

    def test_return_right_list_of_paperwork(self):
        user = User.objects.get(username='testuser@mail.com')
        service = Service.objects.all().first()
        paperwork = Paperwork.objects.all().first()
        pw_service = Paperwork_Service.objects.get(service=service, paperwork=paperwork)
        new_paperwork_service_user = Paperwork_Service_User(user=user, pw_service=pw_service)
        new_paperwork_service_user.save()
        paperwork_service_user  = Paperwork_Service_User.objects.filter(user=user, pw_service__service=service)
        list_of_paperwork = []
        for item in paperwork_service_user:
            list_of_paperwork.append(item.pw_service.paperwork.name)
        self.client.force_login(user)
        response = self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service.id})
        self.assertCountEqual(json.loads(response.content.decode('utf-8')), list_of_paperwork)


class AddToPaperWorksTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_fake_service_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 999
        paperwork_name = 'Identification Document'
        with self.assertRaises(IntegrityError): 
            response = self.client.get(reverse('add_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})

    def test_anonymous_user_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        service_id = 5
        paperwork_name = 'Identification Document'
        with self.assertRaises(ValueError): 
            response = self.client.get(reverse('add_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})

    def test_paperwork_is_added_with_success(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 5
        paperwork_name = 'Identification Document'
        pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
        response = self.client.get(reverse('add_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})
        documents = Paperwork_Service_User.objects.filter(user=user, pw_service=pw_service)
        paperwork_list = []
        for item in documents:
            paperwork_list.append(item.pw_service.paperwork.name)
        self.assertEqual(paperwork_name in paperwork_list, True)
  

class RemoveToPaperWorkTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def setUp(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 5
        paperwork_name = 'Identification Document'
        pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
        self.client.get(reverse('add_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})

    def test_fake_service_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 999
        paperwork_name = 'Identification Document'
        pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
        with self.assertRaises(AttributeError):
            self.client.get(reverse('remove_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})

    def test_anonymous_user_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.logout()
        service_id = 5
        paperwork_name = 'Identification Document'
        pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
        with self.assertRaises(TypeError):
            self.client.get(reverse('remove_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})
        

    def test_paperwork_is_removed_with_success(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 5
        paperwork_name = 'Identification Document'
        pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
        self.client.get(reverse('remove_to_paperworks'), {'user':user, 'paperwork': paperwork_name, 'service_id':service_id})
        documents = Paperwork_Service_User.objects.filter(user=user, pw_service=pw_service)
        paperwork_list = []
        for item in documents:
            paperwork_list.append(item.pw_service.paperwork.name)
        self.assertEqual(paperwork_name not in paperwork_list, True)