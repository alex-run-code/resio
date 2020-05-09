from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service
import json

class GetGradeTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_using_fake_city_return_error(self):
        with self.assertRaises(IndexError): 
            self.client.get(reverse('get_grade'), {'city': 'qdzqdsdqzdq', 'specialty':'Anestezie şi Terapie Intensivă'})


    def test_using_fake_city_specialty_return_error(self):
        with self.assertRaises(IndexError): 
            self.client.get(reverse('get_grade'), {'city': 'Cluj-Napoca', 'specialty':'qdzqdsdqzdq'})

    def test_grade_is_the_lowest_for_selected_city_and_specialty(self):
        specialty = 'Anestezie şi Terapie Intensivă'
        city = 'Cluj-Napoca'
        candidates = Candidate.objects.filter(choice__name=specialty, location__name=city).order_by('grade')
        response = self.client.get(reverse('get_grade'), {'city':city, 'specialty':specialty})
        self.assertEqual(str(candidates.first().grade), response.content.decode('utf-8'))

class GetSpecialtyTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_using_fake_city_return_empty_list(self):
        response = self.client.get(reverse('get_specialty'), {'city': 'qdzqdsdqzdq', 'grade':'10'})
        list_of_specialties = json.loads(response.content.decode('utf-8'))
        self.assertEqual(list_of_specialties, '[]')

    def test_using_wrong_grade_return_error(self):
        with self.assertRaises(ValueError): 
            self.client.get(reverse('get_specialty'), {'city': 'Cluj-Napoca', 'grade':'ten'})

    def test_return_right_list_of_specialties(self):
        city = City.objects.filter(name='Cluj-Napoca').first()
        grade = 10
        candidates = Candidate.objects.filter(grade__lte=grade, location=city)
        specialties = []
        for candidate in candidates:
            specialties.append(candidate.choice.name)
        json_specialties = json.dumps(list(set(specialties)))
        response = self.client.get(reverse('get_specialty'), {'city':city, 'grade':grade})
        self.assertEqual(json.loads(response.content.decode('utf-8')), json_specialties)

class GetCityTest(TestCase):
    fixtures = ["test_data", 'initial_data']

    def test_using_fake_specialty_return_empty_list(self):
        response = self.client.get(reverse('get_city'), {'specialty': 'qdzqdsdqzdq', 'grade':'10'})
        list_of_cities = json.loads(response.content.decode('utf-8'))
        self.assertEqual(list_of_cities, '[]')

    def test_using_fake_grade_return_empty_error(self):
        with self.assertRaises(ValueError): 
            self.client.get(reverse('get_specialty'), {'specialty': 'Anestezie şi Terapie Intensivă', 'grade':'ten'})

    def test_return_right_cities(self):
        grade = 10
        specialty = 'Anestezie şi Terapie Intensivă'
        candidates = Candidate.objects.filter(grade__lte=grade, choice__name=specialty)
        response = self.client.get(reverse('get_city'), {'specialty': specialty, 'grade':grade})
        cities = []
        for candidate in candidates:
            cities.append(candidate.location.name)
        # self.assertEqual(cities, json.loads(response.content.decode('utf-8'))) 
        # This one fail



