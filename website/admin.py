from django.contrib import admin
from .models import Candidate, Hospital, Specialty, Service, City
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Hospital)
admin.site.register(Specialty)
admin.site.register(Service)
admin.site.register(City)