from django.db import models
from autore.models import Autore
import datetime

# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=20)

    def __str__(self):
        return self.categoria

class Keyword(models.Model):
    keyword = models.CharField(max_length=20)

    def __str__(self):
        return self.keyword    

class Articolo(models.Model):
    titolo =  models.CharField(max_length=200)
    id_autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    testo = models.TextField() #max_length=10000
    data = models.DateField(default=datetime.date.today)
    #categorie = models.ManyToManyField(Categoria)
    #keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.titolo

    class Meta:
        get_latest_by  = '-data'

"""
class Appartiene_a(models.Model):
    id_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_articolo', 'categoria'),)
        

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
