from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from households.models import HouseholdElectricityConsumption, HouseholdWaterConsumption, HouseholdsProfile
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate 365 days of dummy data for testing'

    def handle(self, *args, **kwargs):
        # Filter users with user_type 'household'
        household_users = User.objects.filter(userprofile__user_type='household')

        for user in household_users:
            print(user)
            now = datetime.now()  # Initialize with current date and time

            for day in range(365):  # Generate data for the last 365 days
                # Create a new timestamp for each data point with the desired date and time
                timestamp = datetime(now.year, now.month, now.day, 0, 0, 0)

                # Retrieve the associated HouseholdsProfile instance
                household_profile = HouseholdsProfile.objects.get(user=user)

                # Create an instance of HouseholdElectricityConsumption linked to the user profile
                electricity_value = random.uniform(10, 50)  # Random consumption value between 10 and 50 kWh
                electricity_data = HouseholdElectricityConsumption.objects.create(
                    user_profile=household_profile, timestamp=timestamp, value=electricity_value
                )

                # Create an instance of HouseholdWaterConsumption linked to the user profile
                water_value = random.uniform(20, 100)  # Random consumption value between 20 and 100 gallons
                water_data = HouseholdWaterConsumption.objects.create(
                    user_profile=household_profile, timestamp=timestamp, value=water_value
                )

                # Decrement 'now' by one day for the next data point
                now -= timedelta(days=1)
