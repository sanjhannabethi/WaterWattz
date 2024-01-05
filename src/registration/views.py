from datetime import datetime
import random

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from .forms import RegistrationForm
from .models import UserProfile
from households.models import HouseholdsProfile, HouseholdElectricityConsumption, HouseholdWaterConsumption
from industrial.models import IndustrialProfile
from municipal.models import MunicipalProfile
from .forms import LoginForm  # Import the LoginForm you created


def home(request):
    return render(request, 'registration/homepage.html')
def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    user_profile = user.userprofile
                    user_type = user_profile.user_type
                except UserProfile.DoesNotExist:
                    user_type = None

                if user_type == 'household':
                    household_profile, created = HouseholdsProfile.objects.get_or_create(user=user)

                    # Check if HouseholdElectricityConsumption data already exists for the user
                    electricity_consumption_exists = HouseholdElectricityConsumption.objects.filter(
                        user_profile=household_profile).exists()

                    # Check if HouseholdWaterConsumption data already exists for the user
                    water_consumption_exists = HouseholdWaterConsumption.objects.filter(
                        user_profile=household_profile).exists()

                    if not electricity_consumption_exists:
                        # Create an instance of HouseholdElectricityConsumption linked to the user profile
                        electricity_value = random.uniform(10, 50)  # Random consumption value between 10 and 50 kWh
                        electricity_data = HouseholdElectricityConsumption.objects.create(
                            user_profile=household_profile, timestamp=datetime.now(), value=electricity_value
                        )

                    if not water_consumption_exists:
                        # Create an instance of HouseholdWaterConsumption linked to the user profile
                        water_value = random.uniform(20, 100)  # Random consumption value between 20 and 100 gallons
                        water_data = HouseholdWaterConsumption.objects.create(
                            user_profile=household_profile, timestamp=datetime.now(), value=water_value
                        )

                    return redirect('household_dashboard')

                elif user_type == 'industry':
                    return redirect('industry_dashboard')
                elif user_type == 'municipal':
                    return redirect('municipal_dashboard')
                else:
                    error_message = "Invalid user type."

            else:
                error_message = "Invalid login credentials. Please try again."
        else:
            error_message = "Invalid form data. Please check your input."

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
# def login_view(request):
#     error_message = None
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 try:
#                     user_profile = user.userprofile
#                     user_type = user_profile.user_type
#                 except UserProfile.DoesNotExist:
#                     user_type = None
#
#                 if user_type == 'household':
#                     return HttpResponse("Welcome Household User")
#                 elif user_type == 'industry':
#                     return HttpResponse("Welcome Industry User")
#                 elif user_type == 'municipal':
#                     return HttpResponse("Welcome Municipal User")
#                 else:
#                     error_message = "Invalid user type."
#                     logout(user)
#
#             else:
#                 error_message = "Invalid login credentials. Please try again."
#         else:
#             error_message = "Invalid form data. Please check your input."
#
#     else:
#         form = LoginForm()
#
#     return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
#
def register(request):
    error_message = None  # Initialize error_message to None
    user = None  # Initialize user to None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')

        # Check if the email address is already in use
        if User.objects.filter(email=email).exists():
            error_message = "This email address is already registered."
        elif password != password2:
            error_message = "Passwords don't match."
        else:
            try:
                with transaction.atomic():
                    # Create a User object
                    user = User.objects.create_user(username=username, email=email, password=password)

                    user_profile = UserProfile.objects.create(
                        user=user,
                        user_type=user_type
                    )

                    if user_type == 'household':
                        household_profile = HouseholdsProfile.objects.create(user=user)

                        # Check if HouseholdElectricityConsumption data already exists for the user
                        electricity_consumption_exists = HouseholdElectricityConsumption.objects.filter(
                            user_profile=household_profile).exists()

                        # Check if HouseholdWaterConsumption data already exists for the user
                        water_consumption_exists = HouseholdWaterConsumption.objects.filter(
                            user_profile=household_profile).exists()

                        if not electricity_consumption_exists:
                            # Create an instance of HouseholdElectricityConsumption linked to the user profile
                            electricity_value = random.uniform(10, 50)  # Random consumption value between 10 and 50 kWh
                            electricity_data = HouseholdElectricityConsumption.objects.create(
                                user_profile=household_profile, timestamp=datetime.now(), value=electricity_value
                            )

                        if not water_consumption_exists:
                            # Create an instance of HouseholdWaterConsumption linked to the user profile
                            water_value = random.uniform(20, 100)  # Random consumption value between 20 and 100 gallons
                            water_data = HouseholdWaterConsumption.objects.create(
                                user_profile=household_profile, timestamp=datetime.now(), value=water_value
                            )

                    if not error_message:
                        # Log in the user
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            login(request, user)

                            # Redirect to different pages based on user_type
                            if user_type == 'household':
                                return redirect('household_dashboard')
                            elif user_type == 'industry':
                                return redirect('industry_dashboard')
                            elif user_type == 'municipal':
                                return redirect('municipal_dashboard')

            except Exception as e:
                # An error occurred, set the error_message
                error_message = str(e)

    return render(request, 'registration/register.html', {'error_message': error_message})
#
def register(request):
    error_message = None  # Initialize error_message to None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create a User object
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    user_type = form.cleaned_data['user_type']
                    user_profile = UserProfile.objects.create(
                        user=user,
                        user_type=user_type
                    )
                    if user_type == 'household':
                        household_profile = HouseholdsProfile.objects.create(user=user)

                        # Create an instance of HouseholdElectricityConsumption linked to the user profile
                        electricity_value = random.uniform(10, 50)  # Random consumption value between 10 and 50 kWh
                        electricity_data = HouseholdElectricityConsumption.objects.create(
                            user_profile=household_profile, timestamp=datetime.now(), value=electricity_value
                        )

                        # Create an instance of HouseholdWaterConsumption linked to the user profile
                        water_value = random.uniform(20, 100)  # Random consumption value between 20 and 100 gallons
                        water_data = HouseholdWaterConsumption.objects.create(
                            user_profile=household_profile, timestamp=datetime.now(), value=water_value
                        )

                    elif user_type == 'industry':
                        IndustrialProfile.objects.create(user=user)
                    elif user_type == 'municipal':
                        MunicipalProfile.objects.create(user=user)

            except Exception as e:
                # An error occurred, set the error_message
                user.delete()
                error_message = str(e)

            if not error_message:
                # Registration was successful, continue with the rest of your logic
                # Log in the user
                # login(request, user)
                # return redirect('home')  # Redirect to the home page or your desired URL
                return render(request, 'households/authentication/registration_done.html', {'new_user': user})
    else:
        form = RegistrationForm()

    return render(request, 'registration/reg.html', {'form': form, 'error_message': error_message})


def register_view(request):
    error_message = None
    if request.method == 'POST':
        print(request)
        # Get form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']

        if User.objects.filter(email=email).exists():
            error_message = "This email address is already registered."
        elif password != password2:
            error_message = "Passwords don't match."
        else:
            try:
                with transaction.atomic():
                    # Create a User object
                    user = User.objects.create_user(username=username, email=email, password=password)

                    user_profile = UserProfile.objects.create(
                        user=user,
                        user_type=user_type
                    )

                    if user_type == 'household':
                        household_profile = HouseholdsProfile.objects.create(user=user)

                        # Check if HouseholdElectricityConsumption data already exists for the user
                        electricity_consumption_exists = HouseholdElectricityConsumption.objects.filter(
                            user_profile=household_profile).exists()

                        # Check if HouseholdWaterConsumption data already exists for the user
                        water_consumption_exists = HouseholdWaterConsumption.objects.filter(
                            user_profile=household_profile).exists()

                        if not electricity_consumption_exists:
                            # Create an instance of HouseholdElectricityConsumption linked to the user profile
                            electricity_value = random.uniform(10, 50)  # Random consumption value between 10 and 50 kWh
                            electricity_data = HouseholdElectricityConsumption.objects.create(
                                user_profile=household_profile, timestamp=datetime.now(), value=electricity_value
                            )

                        if not water_consumption_exists:
                            # Create an instance of HouseholdWaterConsumption linked to the user profile
                            water_value = random.uniform(20, 100)  # Random consumption value between 20 and 100 gallons
                            water_data = HouseholdWaterConsumption.objects.create(
                                user_profile=household_profile, timestamp=datetime.now(), value=water_value
                            )

                    elif user_type == 'industry':
                        IndustrialProfile.objects.create(user=user)
                    elif user_type == 'municipal':
                        MunicipalProfile.objects.create(user=user)

                    if not error_message:
                        # Log in the user
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            login(request, user)

                            # Redirect to different pages based on user_type
                            if user_type == 'household':
                                return redirect('household_dashboard')
                            elif user_type == 'industry':
                                return redirect('industry_dashboard')
                            elif user_type == 'municipal':
                                return redirect('municipal_dashboard')

            except Exception as e:
                # An error occurred, set the error_message
                error_message = str(e)

    return render(request, 'registration/reg.html', {'error_message': error_message})
