from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from main.models import basketballTeam
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import parser_classes

# Логин
@swagger_auto_schema(
    method='post',
    operation_description="Авторизация пользователя",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_FORM, description='Логин', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('password', openapi.IN_FORM, description='Пароль', type=openapi.TYPE_STRING, format='password', required=True),
    ],
    consumes=["application/x-www-form-urlencoded"],
    responses={
        302: "Перенаправление после авторизации",
        200: "Страница авторизации"
    }
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([FormParser, MultiPartParser])
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                auth.login(request, user)
                messages.success(request, f"{form.cleaned_data['username']}, Вы успешно вошли!")
                return HttpResponseRedirect(request.POST.get('next', reverse('main:main')))
    
    form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

# Регистрация
@swagger_auto_schema(
    method='post',
    operation_description="Регистрация нового пользователя",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_FORM, description='Логин', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('password1', openapi.IN_FORM, description='Пароль', type=openapi.TYPE_STRING, format='password', required=True),
        openapi.Parameter('password2', openapi.IN_FORM, description='Повтор пароля', type=openapi.TYPE_STRING, format='password', required=True),
        openapi.Parameter('first_name', openapi.IN_FORM, description='Имя', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('last_name', openapi.IN_FORM, description='Фамилия', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('fio', openapi.IN_FORM, description="ФИО", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('avatar', openapi.IN_FORM, description='Аватар (необязательно)', type=openapi.TYPE_FILE),
    ],
    consumes=["multipart/form-data"],
    responses={
        302: "Перенаправление после регистрации",
        200: "Страница регистрации"
    }
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([FormParser, MultiPartParser])

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, f"{user.username}, Добро пожаловать!")
            return HttpResponseRedirect(reverse('main:main'))
    
    form = UserRegistrationForm()
    return render(request, 'user/registration.html', {'form': form})

# Профиль
@swagger_auto_schema(
    method='post',
    operation_description="Обновление профиля",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_FORM, description='Логин', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('first_name', openapi.IN_FORM, description='Имя', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('last_name', openapi.IN_FORM, description='Фамилия', type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('avatar', openapi.IN_FORM, description='Аватар', type=openapi.TYPE_FILE),
    ],
    consumes=["multipart/form-data"],
    responses={
        302: "Перенаправление после обновления",
        200: "Страница профиля"
    }
)
@swagger_auto_schema(
    method='get',
    operation_description="Просмотр профиля"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён!")
            return HttpResponseRedirect(reverse('main:main'))
    
    form = ProfileForm(instance=request.user)
    teams = basketballTeam.objects.filter(coach=request.user)
    return render(request, 'user/profile.html', {'form': form, 'teams': teams})

# Выход
@swagger_auto_schema(
    method='get',
    operation_description="Выход из системы",
    responses={
        302: "Перенаправление на главную"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def logout(request):
    auth.logout(request)
    messages.success(request, "До свидания!")
    return redirect(reverse('main:main'))
