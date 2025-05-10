from django.shortcuts import render
from .models import basketballTeam
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import TeamFightBasketball, Tournament
import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    TextSearchIndexType
)
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render, get_object_or_404, redirect
from user.models import User
# Create your views here.

@swagger_auto_schema(method='get', tags=['Основные страницы'])
@api_view(['GET'])
def main(request):
    """
    Главная страница приложения
    """
    return render(request, 'main/index.html')

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_description="Регистрация баскетбольной команды на турнир",
    manual_parameters=[
        openapi.Parameter(
            'fio',
            openapi.IN_FORM,
            description="ФИО тренера",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'name',
            openapi.IN_FORM,
            description="Название команды",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'category',
            openapi.IN_FORM,
            description="Категория команды",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'num_players',
            openapi.IN_FORM,
            description="Количество игроков (минимум 5)",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'players',
            openapi.IN_FORM,
            description="Список игроков (можно через запятую)",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'tournament_id',
            openapi.IN_PATH,
            description="ID турнира",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    consumes=['application/x-www-form-urlencoded'],
    responses={
        200: openapi.Response(description="Успешная регистрация"),
        400: openapi.Response(description="Неверные данные или недостаточно игроков"),
        404: openapi.Response(description="Турнир не найден")
    }
)
@swagger_auto_schema(
    method='get',
    operation_description="Отображение формы регистрации команды",
    manual_parameters=[
        openapi.Parameter(
            'tournament_id',
            openapi.IN_PATH,
            description="ID турнира",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(description="Форма регистрации"),
        404: openapi.Response(description="Турнир не найден")
    }
)
@api_view(['GET', 'POST'])
@parser_classes([FormParser, MultiPartParser])
def register_team(request, tournament_id):
    """
    Регистрация команды на турнир
    - GET: Отображение формы регистрации
    - POST: Создание новой команды с проверкой количества игроков (минимум 5)
    """
    if request.method == 'POST':
        fio = request.POST.get('fio-coach')
        name = request.POST.get('name')
        category = request.POST.get('category')
        num_players = request.POST.get('num_players')
        players = request.POST.get('players')

        tournament = get_object_or_404(Tournament, id=tournament_id)
        coach = User.objects.get(fio=fio)
        if not all([name, category, num_players, players]):
            messages.warning(request, "Заполните все поля формы")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:main')))

        try:
            num_players_int = int(num_players)
        except ValueError:
            messages.warning(request, "Количество игроков должно быть числом")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:main')))

        if num_players_int < 5:
            messages.warning(request, "Минимальное количество игроков - 5")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:main')))

        basketball_team = basketballTeam(
            coach=coach,
            name=name,
            num_players=num_players_int,
            players=players,
            category=category,
            tournament=tournament
        )
        basketball_team.save()
        messages.success(request, "Вы успешно зарегистрировали баскетбольную команду")
        return HttpResponseRedirect(reverse('main:main'))

    context = {
        'tour': get_object_or_404(Tournament, id=tournament_id)
    }
    return render(request, 'main/reg.html', context)

@swagger_auto_schema(method='get', tags=['Турниры'])
@api_view(['GET'])
def show_all_tournaments(request):
    """
    Отображение списка всех турниров
    """
    tr = Tournament.objects.all()

    context = {
        'tr': tr
    }
    return render(request, 'main/tr.html', context)

@swagger_auto_schema(
    method='get',
    tags=['Команды'],
    manual_parameters=[
        openapi.Parameter(
            'tournament_id',
            openapi.IN_PATH,
            description="ID турнира для фильтрации",
            type=openapi.TYPE_INTEGER
        )
    ]
)
@api_view(['GET'])
def filter_teams(request, tournament_id):
    """
    Фильтрация команд по очкам для конкретного турнира
    - Возвращает 4 категории команд (0, 1, 2, 3 очка)
    """
    tournament = Tournament.objects.get(id=tournament_id)
    if len(basketballTeam.objects.filter(tournament=tournament)) < 2:
        messages.warning(request, f"В этом  турнире недостаточно команд ({len(basketballTeam.objects.filter(tournament=tournament))})")
        return HttpResponseRedirect(reverse('main:main'))
    if len(basketballTeam.objects.filter(tournament=tournament)) == 8:
        teams_no_points = basketballTeam.objects.filter(tournament=tournament).filter(points=0)
        team1 = basketballTeam.objects.filter(tournament=tournament).filter(points=1)
        team2 = basketballTeam.objects.filter(tournament=tournament).filter(points=2)
        team3 = basketballTeam.objects.filter(tournament=tournament).filter(points=3)
        len0 = len(teams_no_points)
        t = basketballTeam.objects.filter(tournament=tournament)
        context = {
            'team_no': teams_no_points,
            'team1': team1,
            'team2': team2,
            'team3': team3,
            'len0': len0,
            'len1': len(team1),
            'len2': len(team2),
            'len3': len(team3),
            'len_teams': 8,
            't': t
        }
        return render(request, 'main/basketball_tabl.html', context)
    if len(basketballTeam.objects.filter(tournament=tournament)) == 4:
        teams_no_points = basketballTeam.objects.filter(tournament=tournament).filter(points=0)
        team1 = basketballTeam.objects.filter(tournament=tournament).filter(points=1)
        team2 = basketballTeam.objects.filter(tournament=tournament).filter(points=2)
        t = basketballTeam.objects.filter(tournament=tournament)

        context = {
            'team_no': teams_no_points,
            'team1': team1,
            'team2': team2,
            'len_teams': 4,
            't': t

        }
        return render(request, 'main/basketball_tabl.html', context)
    if len(basketballTeam.objects.filter(tournament=tournament)) == 2:
        teams_no_points = basketballTeam.objects.filter(tournament=tournament).filter(points=0)
        team1 = basketballTeam.objects.filter(tournament=tournament).filter(points=1)
        t = basketballTeam.objects.filter(tournament=tournament)

        context = {
            'team_no': teams_no_points,
            'team1': team1,
            'len_teams': 2,
            't': t
        }
        return render(request, 'main/basketball_tabl.html', context)
    

@swagger_auto_schema(method='get', tags=['Матчи'])
@api_view(['GET'])
def make_fight(request):
    """
    Отображение списка всех матчей
    """
    games = TeamFightBasketball.objects.all()
    context = {
        'games': games
    }
    return render(request, 'main/bb.html', context)


@swagger_auto_schema(
    method='post',
    tags=['Вопросы'],
    operation_description="Запрос через multipart/form-data",
    manual_parameters=[
        openapi.Parameter(
            name='question',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            description="Текст вопроса"
        )
    ]
)
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def answer_question(request):
    """
    Обработка вопросов через Yandex Cloud ML
    - GET: Отображение формы вопроса
    - POST: Получение ответа от ИИ-ассистента
    """
    if request.method == "POST":
        question = request.POST['question']
        print(True)
        load_dotenv()
        sdk = YCloudML(
            folder_id=os.getenv("YANDEX_FOLDER_ID", "RETRACTED"),
            auth=os.getenv("YANDEX_API_KEY", 'RETRACTED'),
        )
        
        assistant = sdk.assistants.get('RETRACTED')
        query = question

        text_index_thread = sdk.threads.create()
        text_index_thread.write(query)
        run = assistant.run(text_index_thread)
        result = run.wait().message
        context = {
            'answer': result.parts
        }
        return render(request, 'main/question.html', context)
    else:
        return render(request, 'main/question.html')
