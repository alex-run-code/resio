from django.db import models

# Create your models here.

class Candidate(models.Model):

    SPECIALITY_CHOICES = [
        ('Pediatric', 'Pediatric'),
        ('Generalist', 'Generalist'),
        ('Ophtalmology', 'Ophtalmology'),
        ('Surgery', 'Surgery'),
        ('Cardiology', 'Cardiology'),
    ]

    LOCATION_CHOICES = [
        ('Alba Iulia', 'Alba Iulia'),
        ('Cluj-Napoca', 'Cluj-Napoca'),
        ('Bucharest', 'Bucharest'),
        ('Mara Mures', 'Mara Mures'),
        ('Timisoara', 'Timisoara'),
    ]

    YEAR_CHOICES = [
        (2017, 2017),
        (2018, 2018),
        (2019, 2019),
        (2020, 2020)
    ]

    first_name = models.CharField(max_length=255, default='None')
    family_name = models.CharField(max_length=255, default='None')
    grade = models.FloatField()
    choice = models.CharField(max_length=255, choices=SPECIALITY_CHOICES)
    location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)

    def __str__(self):
        return self.first_name