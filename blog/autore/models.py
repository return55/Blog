from django.db import models

# Create your models here.

class Autore(models.Model):
    nome = models.CharField(max_length=20, )
    cognome = models.CharField(max_length=20)
    nick = models.CharField(max_length=15, unique=True, help_text='Max 15 caratteri')
    data_nascita = models.DateField() #anno/mese/giorno
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20, help_text='Min 4 caratteri')

    def __str__(self):
        return self.nome + " " + self.cognome + ", " + self.nick

    class Meta:
        get_latest_by  = ['-nome', '-cognome']