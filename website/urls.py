from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('ranking/', views.ranking, name='ranking'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('service/<hospital>/<specialty>/', views.service, name='service'),
    path('research/', views.research, name='research'),
    path('hospital/<hospital>/', views.hospital, name='hospital'),
    path('test/', views.test, name='test'),
    path('ajax/load_hospitals/', views.load_hospitals, name='ajax_load_hospitals'),
    path('ajax/load_specialties/', views.load_specialties, name='ajax_load_specialties'),  # <-- this one here
    path('get_grade/', views.get_grade, name='get_grade'),
]
