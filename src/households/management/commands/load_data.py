import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from municipal.models import MunicipalProfile, Location

class Command(BaseCommand):
    help = 'Create and upload locations for a MunicipalProfile'

    def handle(self, *args, **kwargs):
        username = 'kerala'  # Replace with the username of the MunicipalProfile

        try:
            # Get the user instance with the specified username
            user_instance = User.objects.get(username=username)

            # Try to retrieve the existing MunicipalProfile associated with the user
            existing_municipal_profile = MunicipalProfile.objects.filter(user=user_instance).first()

            if not existing_municipal_profile:
                # Create a new MunicipalProfile if it doesn't exist
                existing_municipal_profile = MunicipalProfile.objects.create(
                    user=user_instance,
                    department='Default Department',
                    location='kerala'
                )

            # Define sectors/locations
            sectors = [
                "Amberpet", "Sanathnagar", "Khairatabad", "Musheerabad", "Nampally",
                "Secunderad", "Financial District", "HITEC City", "Jubilee Hills",
                "Kukatpally", "Patancheru", "Balanagar", "Medchal", "Alwal", "Dilsukhnagar", "LB Nagar"
            ]

            # Create locations for each sector
            for sector in sectors:
                location, created = Location.objects.get_or_create(
                    name=sector,
                    latitude=random.uniform(15, 18),  # Random latitude within a range
                    longitude=random.uniform(75, 80),  # Random longitude within a range
                    description=f"Description for {sector}",
                    municipal_profile=existing_municipal_profile
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Location "{sector}" created successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Location "{sector}" already exists.'))

            self.stdout.write(self.style.SUCCESS('Locations created and uploaded successfully.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username "{username}" does not exist.'))
