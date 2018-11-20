from django.forms import ModelForm
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

import datetime

from autore.models import Autore
from .models import Commento, Articolo

class GenericArticoloForm(forms.ModelForm):

	class Meta:
		model = Articolo
		fields = ('titolo', 'id_autore', 'testo', 'keywords', 'categoria', 'cita')

	def clean_titolo(self):
		titolo = self.cleaned_data.get('titolo')
		if titolo == None:
			raise forms.ValidationError("Devi inserire un titolo")
		return titolo

	def clean_id_autore(self):
		id_autore = self.cleaned_data.get('id_autore')
		if id_autore == None:
			raise forms.ValidationError("Devi selezionare un autore tra quelli esistenti")
		return id_autore

	def clean_testo(self):
		testo = self.cleaned_data.get('testo')
		if testo == None:
			raise forms.ValidationError("Devi inserire il testo")
		return testo

	def clean_categoria(self):
		categoria = self.cleaned_data.get('categoria')
		if categoria == None:
			raise forms.ValidationError("Devi selezionare una categoria")
		return categoria
	
	def clean(self):
		data = super(GenericArticoloForm, self).clean()
		self.clean_titolo()
		self.clean_testo()
		self.clean_categoria()
		return data

class ArticoloAdminChange(GenericArticoloForm):

	def clean(self):
		self.clean_id_autore()
		return super(ArticoloAdminChange, self).clean()


#per gli utenti comuni
class ArticoloAddForm(GenericArticoloForm):
	titolo =  forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':70}))
	#id_autore = forms.ModelChoiceField(queryset=Autore.objects.all(), disabled=True)
	testo = forms.CharField(widget=forms.Textarea(attrs={'rows':40, 'cols':100}), max_length=10000)
	keywords = SimpleArrayField(forms.CharField(max_length=15), delimiter=',', 
								required=False, max_length=10, 
								help_text="Puoi inserire max 10 parole chiave per il tuo articolo separate da ','",
								widget=forms.TextInput(attrs={'size':100}))
	categoria = forms.ChoiceField(choices=Articolo.CATEGORIE_DISPONIBILI)
	cita = forms.ModelMultipleChoiceField(queryset=Articolo.objects.all(), required=False)

	def clean(self):
		return super(ArticoloAddForm, self).clean()

	class Meta:
		model = Articolo
		fields = ('titolo', 'testo', 'keywords', 'categoria', 'cita')

#restituisce tutte le keyword di tutti gli articoli
#senza ripetizioni
def get_all_keywords():
	articoli = Articolo.objects.all()
	keywords = set([])
	for articolo in articoli:
		keywords.update(set(articolo.keywords)) 
	keywords = list(keywords)
	keywords.sort()
	return [ (k ,k) for k in keywords ]

ALTRE_CATEGORIE  = (
		('', '-------'),
        ('CINEMA', 'Cinema'),
        ('SCIENZA', 'Scienza'),
        ('SPORT', 'Sport'),
        ('CUCINA', 'Cucina'),
        ('POLITICA', 'Politica'),
        ('VIAGGI', 'Viaggi'),
)
#form che contienen i campi per la ricerca avanzata.
#view: cerca | cerca.html
#idea per controllo in js:
#almeno un campo deve essere != da vuoto per far partire la ricerca
class CercaArticoloForm(forms.Form):
	parole =  forms.CharField(
		max_length=200, 
		widget=forms.TextInput(attrs={'size':70}),
		help_text="Cerca delle parole nel testo e nel titolo",
		required=False
	)
	id_autore = forms.ModelChoiceField(queryset=Autore.objects.all(), required=False)

	keywords = forms.MultipleChoiceField(choices=get_all_keywords(), required=False)
	categoria = forms.ChoiceField(choices= ALTRE_CATEGORIE, required=False)
	#range di date
	data_inizio = forms.DateField(
			widget=forms.SelectDateWidget(
				years=range(2017, datetime.datetime.today().year+1)),
			required=False)	
	data_fine = forms.DateField(
			widget=forms.SelectDateWidget(
				years=range(2017, datetime.datetime.today().year+1)),
			required=False)	
	citato = forms.IntegerField(
			help_text="Numero minimo di articoli che lo citano",
			min_value=0,
			required=False)

#per gli amministratori
class FormAdminCommento(forms.ModelForm):
	id_articolo = forms.ModelChoiceField(queryset=Articolo.objects.all())
	testo = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':70}), max_length=10000)
	commentatore = forms.CharField(max_length=20)

	class Meta:
		model = Commento
		fields = ('id_articolo', 'testo', 'commentatore')

	#controllo che lo username esista o che sia Anonimo
	def clean_commentatore(self):
		username = self.cleaned_data.get('commentatore')
		if len(Autore.objects.filter(username=username)) == 0 and username != "Anonimo":
			raise forms.ValidationError("Lo username deve appartenere a un autore esistente o essere 'Anonimo'")
		return username

#per gli utenti comuni
class FormCommento(forms.ModelForm):
	testo = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':70}), max_length=10000)

	class Meta:
		model = Commento
		fields = ('testo',)


