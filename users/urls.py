from django.urls import path
from .views import CustomUserRegister

app_name = 'users'

urlpatterns = [
    path('register/', CustomUserRegister.as_view(), name='users-register'),
]