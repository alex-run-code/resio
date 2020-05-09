from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service

class LoadHospitalTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_loading_hospital_with_fake_city_return_nothing(self):
        response = self.client.get(reverse('ajax_load_hospitals'), {'city': 'Cluj-Napoca'})
        pass

    def test_hospital_returned_are_in_right_city(self):
        pass