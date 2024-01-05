from django.core.management.base import BaseCommand
from households.models import HouseholdElectricityConsumption, HouseholdWaterConsumption
from registration.models import UserProfile

class Command(BaseCommand):
    help = 'Flush out previously generated dummy data'

    def handle(self, *args, **kwargs):
        # Delete all records from HouseholdElectricityConsumption and HouseholdWaterConsumption tables
        HouseholdElectricityConsumption.objects.all().delete()
        HouseholdWaterConsumption.objects.all().delete()

        # You can delete other related data if needed

        self.stdout.write(self.style.SUCCESS('Successfully flushed out dummy data'))
