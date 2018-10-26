from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.forms import SimpleArrayField


from autore.models import Autore
import datetime
import re

"""
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
"""
"""
grant usage on schema public to blog;
grant create on schema public to blog;
"""

class Articolo(models.Model):
    titolo =  models.CharField(max_length=200, help_text="Titolo")
    id_autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    testo = models.TextField() #max_length=10000
    data = models.DateField(default=datetime.date.today, editable=False)
    CATEGORIE_DISPONIBILI =(
        ('CINEMA', 'Cinema'),
        ('SCIENZA', 'Scienza'),
        ('SPORT', 'Sport'),
        ('CUCINA', 'Cucina'),
        ('POLITICA', 'Politica'),
        ('VIAGGI', 'Viaggi'),
    )
    keywords = ArrayField(models.CharField(max_length=15, blank=True), max_length=10, help_text="Puoi inserire max 10 parole chiave per il tuo articolo")
    categoria = models.CharField(max_length=8, choices=CATEGORIE_DISPONIBILI, help_text="Categoria")
    citazioni = models.ManyToManyField('self', blank=True, symmetrical=False)

    class Meta:
        verbose_name_plural = 'Articoli'

    def get_nick_autore(self):
        return Autore.objects.get(pk=self.id_autore).get_nick()
    get_nick_autore.boolean = False
    get_nick_autore.short_description = 'Nick Autore'
    
    #r',\\s+'
    def __str__(self):
        return self.titolo

    class Meta:
        get_latest_by  = '-data'

class Commento(models.Model):
    id_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    testo = models.TextField()
    data = models.DateField(default=datetime.date.today, editable=False)
    commentatore = models.CharField(max_length=15, help_text="Nick name") #nick dell'autore, altrimenti inventato

    class Meta:
        unique_together = (('id_articolo', 'id'),)
        verbose_name_plural = 'Commenti'


    def __str__(self):
        return self.id_articolo.titolo + " " + self.commentatore
