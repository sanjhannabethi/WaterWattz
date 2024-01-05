from django.urls import path

from registration import views

urlpatterns = [
    # path('register/', views.register, name='register'),
path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='homepage'),
]
