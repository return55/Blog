import datetime

from django.test import TestCase
from django.utils import timezone

from articolo.models import Articolo
from .models import Autore



class AutoreModelTests(TestCase):
	"""
	#controllo che per gli articoli votati da ogni autore, il numero dei
	#voti sia almeno 1.
	#Serve solo per individuare errori, non garantisce la correttezza dei dati.
	def test_problemi_in_articoli_votati (self):
		tutti_autori = Autore.objects.all()
		for autore in tutti_autori:
			#articoli che ha votato
			for articolo in autore.articoli_votati:
				self.assertIs(articolo.numero_voti > 0, False,
						msg="Non risulta che l'autore "+ autore.username + "abbia votato "+
							"l'articolo '"+ articolo.titolo + "'")		
	"""
	