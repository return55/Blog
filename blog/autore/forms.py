from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

import datetime

from .models import Autore
from articolo.models import Commento

class BaseFormAutore(forms.ModelForm):

	class Meta:
		model = Autore
		fields = ('username', 'email')
	

class RegisterForm(BaseFormAutore):
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)

	class Meta:
		model = Autore
		fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'is_admin', 'is_active')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Le passwords non corrispondono")
		return password2

	def clean(self):
		self.clean_password2()
		return super(RegisterForm, self).clean()

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(BaseFormAutore):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Autore
		fields = ('username', 'password', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'is_admin', 'is_active')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

	def clean(self):
		self.clean_password()
		return super(UserAdminChangeForm, self).clean()

class RegistrationForm(BaseFormAutore):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput)
	first_name = forms.CharField(label='Nome',max_length=20)
	last_name = forms.CharField(label='Cognome',max_length=20)
	bio = forms.CharField(label='Biografia',widget=forms.Textarea, required=False)
	profilo_pubblico = forms.BooleanField(required=False)

	class Meta:
		model = Autore
		fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico')
		
	
	def clean(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		print("Password:")
		print(password)
		print("Password 2:")
		print(password2)
		if password != password2:
			raise forms.ValidationError("Le passwords non corrispondono")
		return super(RegistrationForm, self).clean()
	
	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
	
	

class SettingsForm(BaseFormAutore):
	username = forms.CharField(max_length=20)
	email = forms.EmailField(widget=forms.EmailInput)
	first_name = forms.CharField(label='Nome',max_length=20)
	last_name = forms.CharField(label='Cognome',max_length=20)
	bio = forms.CharField(label='Biografia',widget=forms.Textarea, required=False)
	profilo_pubblico = forms.BooleanField(required=False)

	class Meta:
		model = Autore
		fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico')

	def clean(self):
		return super(SettingsForm, self).clean()



#form che contienen i campi per la ricerca avanzata.
#view: cerca | cerca.html
#idea per controllo in js:
#almeno un campo deve essere != da vuoto per far partire la ricerca
class CercaAutoreForm(forms.Form):
	username = forms.CharField(max_length=20, required=False)
	email = forms.EmailField(widget=forms.EmailInput, required=False)
	first_name = forms.CharField(label='Nome',max_length=20, required=False)
	last_name = forms.CharField(label='Cognome',max_length=20, required=False)
	#range di date
	data_inizio = forms.DateField(
		widget=forms.SelectDateWidget(
			years=range(2017, datetime.datetime.today().year+1)),
			required=False)	
	data_fine = forms.DateField(
		widget=forms.SelectDateWidget(
			years=range(2017, datetime.datetime.today().year+1)),
			required=False)	