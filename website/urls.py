from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('ranking/', views.ranking, name='ranking'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
]
