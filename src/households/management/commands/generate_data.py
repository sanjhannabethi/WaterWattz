from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from households.models import HouseholdsProfile, HouseholdElectricityConsumption, HouseholdWaterConsumption
import random
import time
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate simulated data for users'

    def handle(self, *args, **kwargs):
        while True:
            # Iterate through all users and generate data for each
            for user in User.objects.filter(userprofile__user_type='household'):
                # Simulate electricity and water consumption data
                electricity_value = random.uniform(0.5, 2.0)  # Replace with your logic
                water_value = random.uniform(5.0, 15.0)  # Replace with your logic

                # Get or create the user's household profile
                household_profile, created = HouseholdsProfile.objects.get_or_create(user=user)

                # Create records for electricity and water consumption
                timestamp = datetime.now()
                HouseholdElectricityConsumption.objects.create(user_profile=household_profile, timestamp=timestamp, value=electricity_value)
                HouseholdWaterConsumption.objects.create(user_profile=household_profile, timestamp=timestamp, value=water_value)

                self.stdout.write(self.style.SUCCESS(f'Simulated data for User {user.username}: Electricity={electricity_value:.3f} kWh, Water={water_value:.3f} gallons'))

            # Adjust the sleep time to run every 1 minute
            time.sleep(60)
