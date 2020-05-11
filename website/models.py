from django.db import models
from django.conf import settings


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ', ' + self.service.hospital.name + ', ' + self.service.specialty.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):

    YEAR_CHOICES = [
        (2017, 2017),
        (2018, 2018),
        (2019, 2019),
        (2020, 2020)
    ]

    first_name = models.CharField(max_length=255, default=' - ')
    family_name = models.CharField(max_length=255, default=' - ')
    grade = models.FloatField()
    choice = models.ForeignKey('Specialty', on_delete=models.CASCADE)
    location = models.ForeignKey('City', on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES)

    def __str__(self):
        return self.first_name


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    about = models.TextField(max_length=2550)

    def __str__(self):
        return self.name


class Paperwork(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE)
    chief_name = models.CharField(max_length=255)
    chief_surname = models.CharField(max_length=255)
    residanatms_url = models.CharField(max_length=255)

    def __str__(self):
        return self.hospital.name + ', ' + self.specialty.name


class Paperwork_Service(models.Model):
    paperwork = models.ForeignKey(
        'Paperwork',
        on_delete=models.CASCADE
        )
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.paperwork.name + ' | ' + self.service.hospital.name + ' | ' + self.service.specialty.name


class Paperwork_Service_User(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    pw_service = models.ForeignKey(
        'Paperwork_Service',
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.pw_service.paperwork.name + ' | ' + self.user.username + ' | ' + str(self.pw_service.service.id)
