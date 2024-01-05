from django.contrib import admin
from .models import HouseholdsProfile, HouseholdElectricityConsumption, HouseholdWaterConsumption

# Register your models here.
admin.site.register(HouseholdsProfile)
admin.site.register(HouseholdElectricityConsumption)
admin.site.register(HouseholdWaterConsumption)