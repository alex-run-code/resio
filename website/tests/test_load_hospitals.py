from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service
from bs4 import BeautifulSoup

class LoadHospitalTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_loading_hospital_with_fake_city_return_nothing(self):
        response = self.client.get(reverse('ajax_load_hospitals'), {'city': 'xxx'})
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        options = soup.find_all('option')
        hospital_list = []
        for option in options:
            hospital_list.append(option.get_text())
        del hospital_list[0]
        self.assertEqual(len(hospital_list), 0)
        

    def test_hospital_returned_are_in_right_city(self):
        response = self.client.get(reverse('ajax_load_hospitals'), {'city': 'Cluj-Napoca'})
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        options = soup.find_all('option')
        hospital_list = []
        for option in options:
            hospital_list.append(option.get_text())
        del hospital_list[0]
        for item in hospital_list:
            hospital = Hospital.objects.filter(name=item).first()
            city = City.objects.filter(name='Cluj-Napoca').first()
            self.assertEqual(hospital.city, city)