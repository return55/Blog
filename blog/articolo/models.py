from django.db import models
from autore.models import Autore
import datetime

"""
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
"""
"""
grant usage on schema public to blog;
grant create on schema public to blog;
"""

# Create your models here.
class Keyword(models.Model):
    keyword = models.CharField(max_length=20)

    def __str__(self):
        return self.keyword    

class Articolo(models.Model):
    titolo =  models.CharField(max_length=200)
    id_autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    testo = models.TextField() #max_length=10000
    data = models.DateField(default=datetime.date.today)
    CATEGORIE_DISPONIBILI =(
        ('CINEMA', 'Cinema'),
        ('SCIENZA', 'Scienza'),
        ('SPORT', 'Sport'),
        ('CUCINA', 'Cucina'),
        ('POLITICA', 'Politica'),
        ('VIAGGI', 'Viaggi'),
    )
    categoria = models.CharField(max_length=8, choices=CATEGORIE_DISPONIBILI)
    #keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.titolo

    class Meta:
        get_latest_by  = '-data'

"""
class Contiene(models.Model):
    id_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_articolo', 'keyword'),)
"""   
class Cita(models.Model):
    id_articolo1 =  models.ForeignKey(Articolo, on_delete=models.CASCADE,related_name='cita')
    id_articolo2 =  models.ForeignKey(Articolo, on_delete=models.CASCADE,related_name='è_citato')

    class Meta:
        unique_together = (('id_articolo1', 'id_articolo2'),)

class Commento(models.Model):
    id_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    testo = models.TextField()
    data = models.DateField(default=datetime.date.today)
    commentatore = models.CharField(max_length=15) #nick dell'autore, altrimenti inventato

    class Meta:
        unique_together = (('id_articolo', 'id'),)

    def __str__(self):
        return self.id_articolo + " " + self.commentatore
