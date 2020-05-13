from django.shortcuts import render
from website.models import Candidate, Hospital, Service, Specialty
from website.models import City, Favorite, Paperwork_Service, Paperwork
from website.models import Paperwork_Service_User
from .filters import RankingFilter
from django.http import JsonResponse, HttpResponse
import json
import names
import random
from django.core.paginator import Paginator
from django.db.utils import IntegrityError


def index(request):  # pragma: no cover
    ''' Homepage, contains a presenation of the site. '''
    return render(request, 'website/index.html')


def contact(request):  # pragma: no cover
    ''' Contact page, contains a way to contact us. '''
    return render(request, 'website/contact.html')


def profile(request):  # pragma: no cover
    ''' Profile page, contains the favorite of the user. '''
    user = request.user
    paperwork_collected = Paperwork_Service_User.objects.filter(user=user)
    favorites = Favorite.objects.filter(user=user)
    context = {
        'favorites': favorites,
        'paperwork_collected': paperwork_collected,
    }
    return render(request, 'account/profile.html', context)


def ranking(request):  # pragma: no cover
    '''
    The ranking page contains the algorithm allowing the student
    to get their grade, their city and their specialty, and the
    rankings of the precedent years.
    '''
    specialties = Specialty.objects.all()
    candidates = Candidate.objects.all()
    cities = City.objects.all()
    myFilter = RankingFilter(request.GET, queryset=candidates)
    candidates = myFilter.qs
    p_candidates = Paginator(candidates, 15)
    page_number = request.GET.get('page')
    context = {
        'candidates': p_candidates.get_page(page_number),
        'myFilter': myFilter,
        'specialties': specialties,
        'cities': cities,
    }
    return render(request, 'website/ranking.html', context)


def research(request):  # pragma: no cover
    ''' Allow the user to research a hospital and a specialty. '''
    hospitals = Hospital.objects.all()
    services = Service.objects.all()
    context = {
        'hospitals': hospitals,
        'services': services,
    }
    return render(request, 'website/research.html', context)


def service(request, hospital, specialty):  # pragma: no cover
    '''
    The page of a selected service (hospital+specialty), containing
    informations about the hospital, the paperwork, the key people, etc.
    '''
    service = Service.objects.filter(
        hospital__name=hospital,
        specialty__name=specialty).first()
    hospital_info = service.hospital
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(
            service=service,
            user=request.user).first()
    else:
        favorite = []
    documents = Paperwork_Service.objects.filter(service=service)
    context = {
        'service': service,
        'hospital_name': str(hospital),
        'city': hospital_info.city,
        'specialty': specialty,
        'chief_name': service.chief_name,
        'chief_surname': service.chief_surname,
        'residanatms_url': service.residanatms_url,
        'website': hospital_info.website,
        'address': hospital_info.address,
        'description': hospital_info.about,
        'favorite': favorite,
        'documents': documents,
    }
    return render(request, 'website/service.html', context)


def hospital(request, hospital):  # pragma: no cover
    '''
    Hospital's page, allow the user to chose
    a specialty from selected hospital.
    '''
    hospital_info = Hospital.objects.filter(name=hospital).first()
    if not hospital_info:
        context = {
            'title': 'Unknown hospital',
            'message': 'We didnt find this hospital',
        }
        return render(request, 'website/error.html', context)
    services = Service.objects.filter(hospital__name=hospital)
    context = {
        'hospital_name': str(hospital),
        'city': hospital_info.city,
        'services': services,
    }
    return render(request, 'website/hospital.html', context)


def load_hospitals(request):
    '''
    Load the hospitals and display them in a select button
    used in the research page.
    '''
    city = request.GET.get('city')
    hospitals = Hospital.objects.filter(
        city__name=city).order_by('name')
    return render(
        request,
        'website/load_hospitals.html',
        {'hospitals': hospitals})


def load_specialties(request):
    '''
    Load the specialties and display them in a select button
    used in the research page.
    '''
    hospital = request.GET.get('hospital')
    services = Service.objects.filter(
        hospital__name=hospital).order_by('specialty')
    return render(request, 'website/load_specialties.html', {
        'services': services})


def get_grade(request):
    '''
    Receive a city and a specialty, then return the lowest grade
    obtained by a student who chose said specialty in said city
    in the precedent years.
    '''
    city = City.objects.filter(name=request.GET.get('city')).first()
    specialty = Specialty.objects.filter(
        name=request.GET.get('specialty')).first()
    candidates = Candidate.objects.filter(
        choice=specialty, location=city).order_by('grade')
    try:
        grade = candidates[0].grade
        return HttpResponse(grade)
    except(IndexError):
        return HttpResponse('empty')



def get_specialty(request):
    '''
    Receive a grade and a city, then return the list of specialties
    selected by students who chose said city and obtained a grade
    equal or inferior to the inputed grade, during precedent years.
    '''
    city = City.objects.filter(name=request.GET.get('city')).first()
    grade = request.GET.get('grade')
    candidates = Candidate.objects.filter(grade__lte=grade, location=city)
    specialties = []
    for candidate in candidates:
        specialties.append(candidate.choice.name)
    json_specialties = json.dumps(list(set(specialties)))
    return JsonResponse(json_specialties, safe=False)


def get_city(request):
    '''
    Receive a specialty and a grade, then return the list of cities
    selected by students who chose said specialty and obtained a grade
    equal or inferior to the inputed grade, during precedent years.
    '''
    specialty = Specialty.objects.filter(
        name=request.GET.get('specialty')).first()
    grade = request.GET.get('grade')
    candidates = Candidate.objects.filter(grade__lte=grade, choice=specialty)
    cities = []
    for candidate in candidates:
        cities.append(candidate.location.name)
    json_cities = list(set(cities))
    return JsonResponse(json_cities, safe=False)


def add_to_favorites(request):
    ''' Add to the user's favorite the selected service. '''
    if request.method != 'POST':  # Warning : ajax is using GET method.
        return HttpResponse(status=500)
    user = request.user
    try:
        service = Service.objects.filter(
            hospital__name=request.POST.get('hospital'),
            specialty__name=request.POST.get('specialty')).first()
        new_favorite = Favorite(user=user, service=service)
        new_favorite.save()
        return HttpResponse('added')
    except IntegrityError:
        return HttpResponse(status=500)
    except ValueError:
        return HttpResponse(status=500)


def get_list_of_paperwork(request):
    ''' Add to the user's favorite the selected service. '''
    user = request.user
    service_id = request.GET.get('service_id')
    user_documents = Paperwork_Service_User.objects.filter(
        user=user, pw_service__service=service_id)
    user_documents_list = []
    for document in user_documents:
        user_documents_list.append(document.pw_service.paperwork.name)
    return JsonResponse(user_documents_list, safe=False)


def add_to_paperworks(request):
    '''
    Add to the user's collected paperwork
    the selected document, for a specific service.
    '''
    user = request.user
    paperwork_name = request.GET.get('paperwork')
    service_id = request.GET.get('service_id')
    pw_service = Paperwork_Service.objects.filter(
        service=service_id, paperwork__name=paperwork_name).first()
    new_paperwork = Paperwork_Service_User(user=user, pw_service=pw_service)
    new_paperwork.save()
    return HttpResponse('Document added')


def remove_to_paperworks(request):
    '''
    Remove from the user's collected paperwork
    the selected document, for a specific service.
    '''
    user = request.user
    paperwork_name = request.GET.get('paperwork')
    service_id = request.GET.get('service_id')
    pw_service = Paperwork_Service.objects.filter(
        service=service_id, paperwork__name=paperwork_name).first()
    document = Paperwork_Service_User.objects.filter(
        user=user, pw_service=pw_service).first()
    document.delete()
    return HttpResponse('Document deleted')


def remove_from_fav(request):
    ''' Remove from the user's favorite the selected service. '''
    favorite = Favorite.objects.filter(
        id=request.GET.get('favorite_id')).first()
    favorite.delete()
    return HttpResponse('Favorite deleted')


def add_100_random_candidates():  # pragma: no cover
    '''
    For testing only. Add 100 fake candidates to the database with random name,
    surname, city, specialty, grade and year.
    '''
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
        print(
            new_candidate.first_name,
            ' ',
            new_candidate.family_name, ' : added')


def add_paperwork_for_each_service():
    '''For testing only. Add 5 generic document to each service.'''
    services = Service.objects.all()
    paperworks = Paperwork.objects.all()
    for service in services:
        for paperwork in paperworks:
            new_paperwork_service = Paperwork_Service(
                paperwork=paperwork, service=service)
            new_paperwork_service.save()
            print(paperwork.name, ' added for ', service.hospital.name)
