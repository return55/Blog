from django.forms import ModelForm
from django import forms

from autore.models import Autore
from .models import Commento, Articolo

class GenericArticoloForm(forms.ModelForm):

	class Meta:
		model = Articolo
		fields = ('titolo', 'id_autore', 'testo', 'keywords', 'categoria', 'citazioni')

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
		print(self.cleaned_data.get('testo'))
		testo = self.cleaned_data.get('testo')
		if testo == None:
			raise forms.ValidationError("Devi inserire il testo")
		return testo

	def clean_categoria(self):
		#print(self.cleaned_data.get('categoria').__str__())
		categoria = self.cleaned_data.get('categoria')
		if categoria == None:
			print("ciao")
			raise forms.ValidationError("Devi selezionare una categoria")
		return categoria

	def clean(self):
		print("*****************************")
		data = super(GenericArticoloForm, self).clean()
		self.clean_titolo()
		self.clean_id_autore()
		self.clean_testo()
		self.clean_categoria()	
		return data

#l'autore una volta selezionato, non si puo' piu' cambiare
class ArticoloAdminChange(GenericArticoloForm):

	def clean(self):
		print("*****************************")
		return super(ArticoloAdminChange, self).clean()
