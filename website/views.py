from django.shortcuts import render
from website.models import Candidate, Hospital, Service, Specialty
from .filters import RankingFilter
from django.http import JsonResponse, HttpResponse
import json
from django.views.generic import ListView, CreateView, UpdateView


# Create your views here.



def index(request):
    return render(request, 'website/index.html')

def profile(request):
    cities = [
        'Cluj-Napoca',
        'Alba-Iulia',
        'Bucharest',
        'Maramures',
        'Oas',

        ]
    context = {
        'cities':cities
    }
    return render(request, 'account/profile.html', context)

def contact(request):
    return render(request, 'website/contact.html')

def ranking(request):
    candidates = Candidate.objects.all()
    myFilter = RankingFilter(request.GET, queryset=candidates)
    candidates = myFilter.qs
    context = {
        'candidates':candidates,
        'myFilter':myFilter,
    }
    return render(request, 'website/ranking.html', context)

def research(request):
    hospitals = Hospital.objects.all()
    services = Service.objects.all()
    context = {
        'hospitals':hospitals,
        'services':services,
    }
    return render(request, 'website/research.html', context)

def service(request, hospital, specialty):
    service = Service.objects.filter(hospital__name=hospital, specialty__name=specialty)[0]
    hospital_info = Hospital.objects.filter(name=hospital)[0]
    context = {
        'hospital_name':str(hospital),
        'city': hospital_info.city,
        'specialty':specialty,
        'chief_name':service.chief_name,
        'chief_surname':service.chief_surname,
        'residanatms_url':service.residanatms_url,
        'website':hospital_info.website,
        'address':hospital_info.address,
        'description': hospital_info.about
    }
    return render(request, 'website/service.html', context)

def hospital(request, hospital):
    hospital_info = Hospital.objects.filter(name=hospital)[0]
    services = Service.objects.filter(hospital__name=hospital)
    context = {
        'hospital_name':str(hospital),
        'city': hospital_info.city,
        'services':services,
    }
    return render(request, 'website/hospital.html', context)


def test(request):
    return render(request, 'website/test.html')

def load_hospitals(request):
    city = request.GET.get('city')
    hospitals = Hospital.objects.filter(city=city).order_by('name')
    return render(request, 'website/load_hospitals.html', {'hospitals': hospitals})

def load_specialties(request):
    hospital = request.GET.get('hospital')
    services = Service.objects.filter(hospital__name=hospital).order_by('specialty')
    return render(request, 'website/load_specialties.html', {'services': services})



