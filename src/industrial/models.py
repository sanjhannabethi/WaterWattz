from django.db import models
from django.conf import settings

class IndustrialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='industrial_profile')
    company_name = models.CharField(max_length=100)
    industry_sector = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    # Add additional fields specific to Industrial profile here

    def __str__(self):
        return f'Industrial Profile of {self.company_name}'

class Sector(models.Model):
    industry_profile = models.ForeignKey(IndustrialProfile, on_delete=models.CASCADE, related_name='sectors')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Sensor(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sensor_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.sensor_id



