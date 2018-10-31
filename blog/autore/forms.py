from django.forms import ModelForm
from .models import Autore
from django.contrib.auth.models import User

#forse devo aggiungere la password
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class AutoreForm(ModelForm):
    class Meta:
        model = Autore
        fields = ('bio', 'profilo_pubblico')