from django.forms import ModelForm
from .models import Commento

class FormCommento(ModelForm):
	class Meta:
		model = Commento
		fields = ['id_articolo', 'testo', 'data', 'commentatore']