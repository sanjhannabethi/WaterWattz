from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HouseholdsProfile, HouseholdElectricityConsumption, HouseholdWaterConsumption
from datetime import datetime, timedelta
from django.contrib import messages

@login_required
def home(request):
    user = request.user
    interval = request.GET.get('interval', '14days')  # Default to 14 days if no interval is specified

    # Calculate the start date and end date based on the selected interval
    if interval == '1week':
        start_date = datetime.now() - timedelta(weeks=1)
    elif interval == '1month':
        start_date = datetime.now() - timedelta(weeks=4)
    elif interval == '6months':
        start_date = datetime.now() - timedelta(weeks=26)
    elif interval == '14days':  # Add this option for the default 14 days
        start_date = datetime.now() - timedelta(weeks=2)
    else:
        # Default to 14 days
        start_date = datetime.now() - timedelta(weeks=2)
    end_date = datetime.now()

    try:
        # Retrieve consumption data based on the selected interval
        electricity_data = HouseholdElectricityConsumption.objects.filter(
            user_profile__user=user, timestamp__range=(start_date, end_date)
        ).order_by('timestamp')

        water_data = HouseholdWaterConsumption.objects.filter(
            user_profile__user=user, timestamp__range=(start_date, end_date)
        ).order_by('timestamp')
    except (HouseholdElectricityConsumption.DoesNotExist, HouseholdWaterConsumption.DoesNotExist):
        # Handle the case where there is no consumption data
        electricity_data = []
        water_data = []

    electricity_values = [data.value for data in electricity_data]
    water_values = [data.value for data in water_data]
    timestamps = [data.timestamp.strftime('%Y-%m-%d %H:%M:%S') for data in electricity_data]
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    household_profile = HouseholdsProfile.objects.get(user__username=user.username)

    # Retrieve electricity consumption data for the user in the last 24 hours.
    electricity_consumption_data = electricity_values[-1] if electricity_values else None

    # Retrieve water consumption data for the user in the last 24 hours.
    water_consumption_data = water_values[-1] if water_values else None

    return render(request, 'households/features/user_dashboard.html', {
        'electricity_values': electricity_values,
        'water_values': water_values,
        'timestamps': timestamps,
        'electricity_consumption_data': electricity_consumption_data,
        'water_consumption_data': water_consumption_data,
        'selected_interval': interval,  # Pass the selected interval to the template
    })

@login_required
def update_consumption_goal(request):
    user_profile = request.user.household_profile  # Get the user's household profile
    consumption_goal = user_profile.consumptiongoal

    if consumption_goal.can_update():
        # Allow the user to update their consumption goals
        if request.method == 'POST':
            # Process and update the goals from the form data
            # ...
            # Save the updated goals
            consumption_goal.save()
            messages.success(request, 'Consumption goals updated successfully.')
            return redirect('profile_dashboard')
    else:
        # Display a message to inform the user they can't update yet
        messages.error(request, 'You can update your consumption goals once every 24 hours.')
        return redirect('profile_dashboard')

    return render(request, 'update_consumption_goal.html', {'consumption_goal': consumption_goal})

# @login_required()
# def user_homepage(request):
#     return render(request, 'households/features/user_dashboard.html')