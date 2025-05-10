from django.urls import path
from .views import registration, login, logout, profile


app_name = 'user'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout')
]