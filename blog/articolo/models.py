from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver

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
class LowerCaseCharField(models.CharField):
    def to_python(self, value):
        value = super(LowerCaseCharField, self).to_python(value)
        return value.lower()

class Articolo(models.Model):
    titolo =  models.CharField(max_length=200, help_text="Titolo", unique=True)
    id_autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    testo = models.TextField() #max_length=10000
    data = models.DateField(default=datetime.date.today, editable=False)
    CATEGORIE_DISPONIBILI = (
        ('CINEMA', 'Cinema'),
        ('SCIENZA', 'Scienza'),
        ('SPORT', 'Sport'),
        ('CUCINA', 'Cucina'),
        ('POLITICA', 'Politica'),
        ('VIAGGI', 'Viaggi'),
    )
    keywords = ArrayField(LowerCaseCharField(max_length=15), blank=True, size=10, help_text="Puoi inserire max 10 parole chiave per il tuo articolo")
    categoria = models.CharField(max_length=8, choices=CATEGORIE_DISPONIBILI, help_text="Categoria")
    cita = models.ManyToManyField('self', blank=True, symmetrical=False)
    #numero di articoli che mi hanno citato
    citato =  models.IntegerField(editable=False, default=0)
    #media dei voti degli utenti
    somma_voti =  models.IntegerField(editable=False, default=0)
    numero_voti = models.IntegerField(editable=False, default=0)

    class Meta:
        get_latest_by  = '-data'
        verbose_name_plural = 'Articoli'

    def get_voto(self):
        if self.numero_voti == 0:
            return 0
        return self.somma_voti / self.numero_voti

    def get_nick_autore(self):
        return self.id_autore.username
    get_nick_autore.boolean = False
    get_nick_autore.short_description = 'Nick Autore'

    def get_num_citazioni(self):
        return len(self.cita.all())
    get_num_citazioni.boolean = False
    get_num_citazioni.short_description = 'Quanti Artcoli Cito'
    
    #r',\\s+'
    def __str__(self):
        return self.titolo

#quando elimino un articolo devo modificare il campo 'citato' degli altri: (citati - 1)
@receiver(post_delete, sender=Articolo)
def aggiorno_citato_altri_del(sender, instance, *args, **kwargs):
    for articolo in instance.cita.all():
        articolo.citato -= 1

#quando creo un articolo devo modificare il campo 'citato' degli altri: (citati + 1)
@receiver(post_save, sender=Articolo)
def aggiorno_citato_altri_add(sender, instance, *args, **kwargs):
    for articolo in instance.cita.all():
        articolo.citato += 1

class Commento(models.Model):
    id_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    testo = models.TextField()
    data = models.DateField(default=datetime.date.today, editable=False)
    commentatore = models.CharField(max_length=15, help_text="Nick name", default="Anonimo") #nick dell'autore, altrimenti anonimo

    class Meta:
        unique_together = (('id_articolo', 'id'),)
        verbose_name_plural = 'Commenti'


    def __str__(self):
        return self.id_articolo.titolo + " " + self.commentatore
