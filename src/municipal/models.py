from django.db import models
from django.conf import settings

class MunicipalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='municipal_profile')
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    # Add additional fields specific to Municipal profile here

    def __str__(self):
        return f'Municipal Profile of {self.department} --> {self.location}'


class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    municipal_profile = models.ForeignKey(MunicipalProfile, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return self.name

class DataReading(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    water_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    electricity_consumption = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reading at {self.location.name} - {self.timestamp}"
