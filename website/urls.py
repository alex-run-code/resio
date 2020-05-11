from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='index'),
    path('ranking/', views.ranking, name='ranking'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('service/<hospital>/<specialty>/', views.service, name='service'),
    path('research/', views.research, name='research'),
    path('hospital/<hospital>/', views.hospital, name='hospital'),
    path('ajax/load_hospitals/', views.load_hospitals, name='ajax_load_hospitals'),
    path('ajax/load_specialties/', views.load_specialties, name='ajax_load_specialties'),
    path('get_grade/', views.get_grade, name='get_grade'),
    path('get_specialty/', views.get_specialty, name='get_specialty'),
    path('get_city/', views.get_city, name='get_city'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('get_list_of_paperwork/', views.get_list_of_paperwork, name='get_list_of_paperwork'),
    path('add_to_paperworks/', views.add_to_paperworks, name='add_to_paperworks'),
    path('remove_to_paperworks/', views.remove_to_paperworks, name='remove_to_paperworks'),
    path('remove_from_fav/', views.remove_from_fav, name='remove_from_fav'),
    path('contact/', views.contact, name='contact'),
]

# url(r'^$', TemplateView.as_view(template_name='static_pages/index.html'), name='home'),

