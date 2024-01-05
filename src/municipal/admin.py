from django.contrib import admin
from .models import MunicipalProfile, Location, DataReading

# Register your models here.

admin.site.register(MunicipalProfile)
admin.site.register(Location)
admin.site.register(DataReading)
