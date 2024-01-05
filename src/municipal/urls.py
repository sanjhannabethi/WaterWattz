# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define the URL pattern for the municipal dashboard view
    path('dashboard/', views.municipal_dashboard, name='municipal_dashboard'),
    path('location/<int:location_id>/', views.location_consumption, name='location_consumption'),
    path('download_pdf/', views.generate_pdf, name='download_pdf'),
    # Add other URL patterns as needed
]
