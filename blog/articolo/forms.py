from django.forms import ModelForm
from .models import Commento

class FormCommento_NoNick(ModelForm):
	class Meta:
		model = Commento
		fields = ['testo']

class FormCommento_ConNick(ModelForm):
	class Meta:
		model = Commento
		fields = ['testo', 'commentatore']
