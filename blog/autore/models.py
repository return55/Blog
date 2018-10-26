from django.db import models
from django.contrib.auth.models import User

import datetime


class Autore(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    data_registrazione = models.DateField(default=datetime.date.today, editable=False)
    bio = models.TextField(blank=True)
    profilo_pubblico = models.BooleanField(default=0)

    class Meta:
        get_latest_by  = ['-(User.objects.get(pk=self.user)).first_name', '-(User.objects.get(pk=self.user)).last_name']
        verbose_name_plural = 'Autori'

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ", " + self.user.username

    def get_nome(self):
        return self.user.first_name

    def get_cognome(self):
        return self.user.last_name

    def get_email(self):
        return self.user.email

    def get_nick(self):
        return self.user.username

