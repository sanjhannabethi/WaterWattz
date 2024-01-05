from django.urls import path

from households import views

urlpatterns = [
    path('homepage', views.home, name='household_dashboard'),

]
