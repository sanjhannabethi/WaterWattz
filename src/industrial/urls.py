
from django.urls import path
from industrial import views

urlpatterns = [
    path('', views.dashboard, name='industry_dashboard')
]
