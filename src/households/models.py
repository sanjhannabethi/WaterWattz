from django.db import models
from django.conf import settings
from django.utils import timezone


class HouseholdsProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='household_profile')
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'Households Profile of {self.user.username}'


class HouseholdElectricityConsumption(models.Model):
    user_profile = models.ForeignKey(HouseholdsProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        formatted_time = self.timestamp.strftime('%Y-%m-%d %I:%M %p')
        return f"Electricity Consumption - User: {self.user_profile.user.username}, Date: {formatted_time}, Value: {self.value: .3f} kWh"


class HouseholdWaterConsumption(models.Model):
    user_profile = models.ForeignKey(HouseholdsProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        formatted_time = self.timestamp.strftime('%I:%M %p')
        return f"Water Consumption - User: {self.user_profile.user.username}, Date: {formatted_time}, Value: {self.value: .3f} gallons"


class ConsumptionGoal(models.Model):
    user_profile = models.OneToOneField('HouseholdsProfile', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    electricity_goal = models.FloatField()
    water_goal = models.FloatField()

    def __str__(self):
        return f'Consumption Goal for {self.user_profile.user.username} - Last Updated: {self.last_updated}'

    def can_update(self):
        # Check if 24 hours have passed since the last update
        return timezone.now() >= self.last_updated + timezone.timedelta(hours=24)