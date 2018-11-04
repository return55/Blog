from django import forms
from django.contrib.auth import (
	authenticate, get_user_model,
	login, logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user  = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("Questo utente non esiste")
		if not user.check_password(password):
			raise forms.ValidationError("Password sbagliata")
		if not user.is_active():
			raise forms.ValidationError("L'utente non e' piu' attivo")
		return super(UserLoginForm, self).clean()