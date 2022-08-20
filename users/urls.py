from django.urls import path
from .views import UserRegisterView, BlacklistRefreshTokenView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/blacklist/', BlacklistRefreshTokenView.as_view(),
         name='logout-blacklist')
]