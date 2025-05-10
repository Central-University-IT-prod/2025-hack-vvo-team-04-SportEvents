from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "fio",
            "username",
            "password1",
            "password2",
            "image"
        )
    
    fio = forms.CharField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "fio",
            "image",
            "username",
        )

    image = forms.ImageField(required=False)
    fio = forms.CharField()
    username = forms.CharField()
