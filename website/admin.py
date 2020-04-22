from django.contrib import admin
from .models import Candidate, Hospital, Specialty, Service, City, Favorite, Paperwork, Paperwork_Service
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Hospital)
admin.site.register(Specialty)
admin.site.register(Service)
admin.site.register(City)
admin.site.register(Favorite)
admin.site.register(Paperwork)
admin.site.register(Paperwork_Service)
