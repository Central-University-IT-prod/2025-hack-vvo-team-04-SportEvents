from django.contrib import admin
from .models import basketballTeam
from .models import TeamFightBasketball
from .models import Tournament
# Register your models here.

admin.site.register(basketballTeam)
admin.site.register(TeamFightBasketball)
admin.site.register(Tournament)