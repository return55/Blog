from django.forms import ModelForm
from django import forms
from django.contrib.postgres.forms import SimpleArrayField
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

	#potrei metterla in post-save
	def aggiorna_articoli_citati(self):
		cita = self.cleaned_data.get('cita')
		for articolo in cita:
			articolo.citato += 1
			articolo.save()
		return None

	def clean(self):
		data = super(GenericArticoloForm, self).clean()
		self.clean_titolo()
		self.clean_testo()
		self.clean_categoria()
		#dopo tutti i controlli, aggiorno 'citato' degli articoli che quello nuovo cita
		self.aggiorna_articoli_citati()
		return data

class ArticoloAdminChange(GenericArticoloForm):

	def clean(self):
		self.clean_id_autore()
		return super(ArticoloAdminChange, self).clean()

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

class FormCommento(forms.ModelForm):
	testo = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':70}), max_length=10000)

	class Meta:
		model = Commento
		fields = ('testo',)


