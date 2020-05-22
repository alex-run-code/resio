from django.test import TestCase
from django.urls import reverse


class LoadHospitalTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_loading_hospital_with_fake_city_return_nothing(self):
        city = 'xxx'
        response = self.client.get(
            reverse('ajax_load_hospitals'),
            {'city': city})
        hospital_list = response.context['hospitals']
        self.assertEqual(len(hospital_list), 0)

    def test_hospital_returned_are_in_right_city(self):
        city = 'Cluj-Napoca'
        response = self.client.get(
            reverse('ajax_load_hospitals'),
            {'city': city})
        hospital_list = response.context['hospitals']
        for item in hospital_list:
            self.assertEqual(item.city.name, city)


class LoadSpecialtyTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_loading_specialty_with_fake_city_return_nothing(self):
        hospital = 'xxx'
        response = self.client.get(
            reverse('ajax_load_specialties'),
            {'hospital': hospital})
        service_list = response.context['services']
        self.assertEqual(len(service_list), 0)

    def test_specialties_returned_are_from_right_hospital(self):
        hospital = 'Spitalul Clinic de Copii'
        response = self.client.get(
            reverse('ajax_load_specialties'),
            {'hospital': hospital})
        service_list = response.context['services']
        for item in service_list:
            self.assertEqual(item.hospital.name, hospital)
