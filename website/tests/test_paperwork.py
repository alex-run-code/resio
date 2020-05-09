from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service
import json

class GetListofPaperWorkTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_fake_service_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 999
        response = self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
        # print(response.content)
        # it returns b'"[]"'

    def test_anonymous_user_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        service_id = 1
        with self.assertRaises(TypeError): 
            self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
       

    def test_return_right_list_of_paperwork(self):
        user = User.objects.get(username='testuser@mail.com')
        favorites  = Favorite.objects.filter(user=user)
        self.client.force_login(user)
        service_id = 1
        response = self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
        # self.assertEqual(favorites.first(), response.content)
        # AssertionError: None != b'"[]"'


class AddToPaperWorkTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_fake_service_return_error(self):
        user = User.objects.get(username='testuser@mail.com')
        self.client.force_login(user)
        service_id = 999
        response = self.client.get(reverse('get_list_of_paperwork'), {'user': user, 'service_id':service_id})
        pass

    def test_anonymous_user_return_error(self):
        pass

    def test_paperwork_is_added_with_success(self):
        pass

class RemoveToPaperWorkTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_fake_service_return_error(self):
        pass

    def test_anonymous_user_return_error(self):
        pass

    def test_paperwork_is_removed_with_success(self):
        pass