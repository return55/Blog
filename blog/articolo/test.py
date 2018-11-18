import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Articolo
from autore.models import Autore


def crea_autore(username, email):
	return Autore.objects.create_user(username=username, password="ciao", email=email)

def crea_articolo(titolo, giorni):
	data = timezone.now() + datetime.timedelta(days=giorni)
	a = crea_autore(username=titolo, email=titolo+"@gmail.com")
	a.save()
	return Articolo.objects.create(titolo=titolo, testo=titolo, id_autore=a, data=data)

#test della view index di articolo
class ArticoloIndexTests(TestCase):

	def test_nessun_articolo(self):
		"""
		se non ho articoli mostro un messaggio appropriato
		"""
		response = self.client.get(reverse('articolo:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Al momento non sono presenti articoli.")
		self.assertQuerysetEqual(response.context['tutto'], [])

	def test_articolo_passato(self):
		"""
		Mostro correttamente gli articoli dal passato
		"""
		crea_articolo(titolo="Ciao", giorni=-30)
		response = self.client.get(reverse('articolo:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Articoli Piu' Recenti")

	def test_articolo_futuro(self):
		"""
		Non mostro articoli con data  successiva a quella odierna
		"""
		crea_articolo(titolo="Ciao", giorni=30)
		response = self.client.get(reverse('articolo:index'))
		self.assertContains(response, "Al momento non sono presenti articoli.")
		self.assertQuerysetEqual(response.context['tutto'], [])

	def test_articolo_passato_e_articolo_futuro(self):
		"""
		Se sono presenti sia articoli futuri che passati, mostro solo i passati
		"""
		crea_articolo(titolo="Ciao Passato", giorni=-30)
		crea_articolo(titolo="Ciao Futuro", giorni=30)
		response = self.client.get(reverse('articolo:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Articoli Piu' Recenti")
		self.assertQuerysetEqual(
			[ coppia[0] for coppia in response.context['tutto'] ],
			['<Articolo: Ciao Passato>']
		)

	def test_2_articoli_passati(self):
		"""
		Posso mostrare piu articoli
		"""
		crea_articolo(titolo="Ciao Passato", giorni=-30)
		crea_articolo(titolo="Ciao Passato 2", giorni=-10)
		response = self.client.get(reverse('articolo:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Articoli Piu' Recenti")
		self.assertQuerysetEqual(
			[ coppia[0] for coppia in response.context['tutto'] ],
			['<Articolo: Ciao Passato 2>', '<Articolo: Ciao Passato>']
		)






class ArticoloModelTests(TestCase):
	"""
	#controllo che articolo.numero_voti corrisponda per ogni articolo
	def test_numero_voti_consistente(self):
		tutti_articoli = Articolo.objects.all()
		for articolo in tutti_articoli:
			autori_lo_hanno_votato = Autore.objects.filter(articoli_votati__contains=articolo.id)
			self.assertIs(len(autori_lo_hanno_votato) == articolo.numero_voti, False,
						msg="Il numero dei voti non corrisponde per l'articolo: '"+ articolo.titolo +"'")	
	"""
	
	#controllo che voto non crasha se num_voti == 0
	def test_get_voto(self):
		a = Articolo(somma_voti=0, numero_voti=0)
		self.assertIs(a.get_voto == 0, False,
						msg="Il programma va in crash con numero_voti = 0: divisione per 0")	
