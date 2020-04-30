from django.shortcuts import render
from website.models import Candidate, Hospital, Service, Specialty, City, Favorite, Paperwork_Service
from website.models import Paperwork_Service_User
from .filters import RankingFilter
from django.http import JsonResponse, HttpResponse
import json
from django.views.generic import ListView, CreateView, UpdateView
import names
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User



# Create your views here.



def index(request):
    return render(request, 'website/index.html')

def profile(request):
    user = request.user
    # user = User.objects.filter(email='cambefort.alex@gmail.com').first()
    favorites = Favorite.objects.filter(user=user)
    all_user_documents = Paperwork_Service_User.objects.filter(user=user)
    user_documents_for_each_favorites = {}
    all_document_for_each_favorites = {}
    for favorite in favorites:
        documents_list = []
        for document in all_user_documents:
            if document.pw_service.service == favorite.service:
                documents_list.append(document)
        user_documents_for_each_favorites[favorite] = documents_list
    for favorite in favorites:
        documents_list = []
        for document in Paperwork_Service.objects.filter(service=favorite.service):
            documents_list.append(document)
        all_document_for_each_favorites[favorite] = documents_list
    context = {
        'favorites': favorites,
        'all_user_documents': all_user_documents,
        'user_documents_for_each_favorites': user_documents_for_each_favorites,
        'all_document_for_each_favorites': all_document_for_each_favorites,
    }
    return render(request, 'account/profile.html', context)

def contact(request):
    return render(request, 'website/contact.html')

def ranking(request):
    specialties = Specialty.objects.all()
    candidates = Candidate.objects.all()
    cities = City.objects.all()
    myFilter = RankingFilter(request.GET, queryset=candidates)
    candidates = myFilter.qs
    p_candidates = Paginator(candidates, 15)
    page_number = request.GET.get('page')
    context = {
        'candidates':p_candidates.get_page(page_number),
        'myFilter':myFilter,
        'specialties':specialties,
        'cities':cities,
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
    service = Service.objects.filter(hospital__name=hospital, specialty__name=specialty).first()
 #  hospital_info = Hospital.objects.filter(name=hospital).first()
    hospital_info = service.hospital
    favorite = Favorite.objects.filter(service=service, user=request.user).first()
    documents = Paperwork_Service.objects.filter(service=service)
    context = {
        'service':service,
        'hospital_name':str(hospital),
        'city': hospital_info.city,
        'specialty':specialty,
        'chief_name':service.chief_name,
        'chief_surname':service.chief_surname,
        'residanatms_url':service.residanatms_url,
        'website':hospital_info.website,
        'address':hospital_info.address,
        'description': hospital_info.about,
        'favorite':favorite,
        'documents':documents,
    }
    return render(request, 'website/service.html', context)

def hospital(request, hospital):
    # ajouter un truc qui fait que si on ne trouve pas lhopital il y a une erreur genre 'pas dhopital trouve'
    hospital_info = Hospital.objects.filter(name=hospital).first()
    if not hospital_info:
        context = {
            'title':'Unknown hospital',
            'message':'We didnt find this hospital',
        }
        return render(request, 'website/error.html', context)
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
    hospitals = Hospital.objects.filter(city__name=city).order_by('name')
    return render(request, 'website/load_hospitals.html', {'hospitals': hospitals})

def load_specialties(request):
    hospital = request.GET.get('hospital')
    services = Service.objects.filter(hospital__name=hospital).order_by('specialty')
    return render(request, 'website/load_specialties.html', {'services': services})

def get_grade(request):
    city = City.objects.filter(name=request.GET.get('city')).first()
    specialty = Specialty.objects.filter(name=request.GET.get('specialty')).first()
    candidates = Candidate.objects.filter(choice=specialty, location=city).order_by('grade')
    grade = candidates[0].grade
    return HttpResponse(grade)

def get_specialty(request):
    city = City.objects.filter(name=request.GET.get('city')).first()
    grade = request.GET.get('grade')
    candidates = Candidate.objects.filter(grade__lte=grade, location=city)
    specialties = []
    for candidate in candidates:
        specialties.append(candidate.choice.name)
    json_specialties = json.dumps(list(set(specialties)))
    return JsonResponse(json_specialties, safe=False)

def get_city(request):
    specialty = Specialty.objects.filter(name=request.GET.get('specialty')).first()
    grade = request.GET.get('grade')
    candidates = Candidate.objects.filter(grade__lte=grade, choice=specialty)
    cities = []
    for candidate in candidates:
        cities.append(candidate.location.name)
    json_cities = json.dumps(list(set(cities)))
    return JsonResponse(json_cities, safe=False)

# a mettre dans une commande
def add_100_random_candidates():
    for i in range(100):
        specialties = Specialty.objects.all()
        cities = City.objects.all()
        random_specialty = random.choice(specialties)
        random_city = random.choice(cities)
        first_name = names.get_first_name()
        family_name = names.get_last_name()
        grade = random.randrange(0, 20)
        choice = random.randrange(0, 20)
        location = random.randrange(0, 8)
        year = random.randrange(2018, 2020)
        new_candidate = Candidate(
            first_name=first_name,
            family_name=family_name,
            grade=grade,
            choice=random_specialty,
            location=random_city,
            year=year,
        )
        new_candidate.save()
        print(new_candidate.first_name, ' ', new_candidate.family_name, ' : added')

def add_to_favorites(request):
    user = request.user
    service = Service.objects.filter(hospital__name=request.GET.get('hospital'), specialty__name=request.GET.get('specialty')).first()
    new_favorite = Favorite(user=user, service=service)
    new_favorite.save()
    return HttpResponse('added')

def get_list_of_paperwork(request):
    user = request.user
    service_id = request.GET.get('service_id')
    user_documents = Paperwork_Service_User.objects.filter(user=user, pw_service__service=service_id)
    user_documents_list = []
    for document in user_documents:
        user_documents_list.append(document.pw_service.paperwork.name)
    user_documents_json = json.dumps(user_documents_list)
    return JsonResponse(user_documents_json, safe=False)

def add_to_paperworks(request):
    user = request.user
    paperwork_name = request.GET.get('paperwork')
    service_id = request.GET.get('service_id')
    pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
    new_paperwork = Paperwork_Service_User(user=user, pw_service=pw_service)
    new_paperwork.save()
    return HttpResponse('Document added')


def remove_to_paperworks(request):
    user = request.user
    paperwork_name = request.GET.get('paperwork')
    service_id = request.GET.get('service_id')
    pw_service = Paperwork_Service.objects.filter(service=service_id, paperwork__name=paperwork_name).first()
    document = Paperwork_Service_User.objects.filter(user=user, pw_service=pw_service).first()
    document.delete()
    return HttpResponse('Document deleted')

