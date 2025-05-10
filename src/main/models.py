from django.db import models
from user.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    is_going_now = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self):
        return f"Турнир {self.name} по адресу {self.address}"
    


class basketballTeam(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    coach = models.ForeignKey(to=User, on_delete=models.CASCADE)
    num_players = models.PositiveSmallIntegerField(default=5)
    points = models.PositiveSmallIntegerField(default=0)
    players = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True)
    is_playing_now = models.BooleanField(default=False)
    tournament = models.ForeignKey(to=Tournament, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Баскетбольная команда"
        verbose_name_plural = "Баскетбольные команды"
        ordering = ['points']
    
    def __str__(self):
        return f"Баскетбольная команда {self.name} на турнир {self.tournament}"
    

class TeamFightBasketball(models.Model):
    team_one = models.ForeignKey(to=basketballTeam, on_delete=models.CASCADE, null=True, related_name='jewel_item_code')
    team_two = models.ForeignKey(to=basketballTeam, on_delete=models.CASCADE, null=True, related_name='jewel_item_name')
    team1_points = models.PositiveSmallIntegerField(default=0)
    team2_points = models.PositiveSmallIntegerField(default=0)
    time = models.PositiveSmallIntegerField(default=40)
    
    class Meta:
        verbose_name = "Баскетбольный матч"
        verbose_name_plural = "Баскетбольные матчи"
    
    def __str__(self):
        return f"Баскетбольный матч между {self.team_one} и {self.team_two}"
      