from django.urls import path, include
from django.contrib import admin
from .views import main, register_team, filter_teams, make_fight, answer_question, show_all_tournaments
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

app_name = 'main'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('reg_team/<int:tournament_id>/', register_team, name='register_team'),
    path('basketball_tabl/<int:tournament_id>/', filter_teams, name="filter_teams_basketball"),
    path('basketball_matchups/', make_fight, name="make_fights"),
    path('answer_question/', answer_question, name="question"),
    path('all_tournaments/', show_all_tournaments, name="show_all_tr"),
]