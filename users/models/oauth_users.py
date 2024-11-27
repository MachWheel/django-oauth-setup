from django.db import models
from django.utils import timezone


class OauthUser(models.Model):
    """Represents an user that signed in using OAuth"""
    first_name = models.CharField("Nome", max_length=150, blank=True)
    last_name = models.CharField("Sobrenome", max_length=150, blank=True)
    email = models.EmailField("Email", unique=True, blank=False)
    service_name = models.CharField(verbose_name="Acesso por", max_length=150)
    date_created = models.DateTimeField(verbose_name="Criado em", default=timezone.now)

    def __str__(self):
        return f'{self.email}'
