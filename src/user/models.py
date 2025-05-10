from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='coach_image', blank=True, null=True)
    fio = models.CharField(max_length=150, null=True, blank=True)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username