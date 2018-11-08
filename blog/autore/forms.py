from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Autore
from articolo.models import Commento

class BaseFormAutore(forms.ModelForm):

	class Meta:
		model = Autore
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = Autore.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("username gia in uso")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Autore.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email gia' in uso")
		return email

	def clean(self):
		data = super(BaseFormAutore, self).clean()
		self.clean_username()
		self.clean_email()
		return data

class RegisterForm(BaseFormAutore):
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)

	class Meta:
		model = Autore
		fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'admin')

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
	#sono disabilitati perche' non riesco a gestire il controllo della clean
	username = forms.CharField(max_length=20, disabled=True)
	email = forms.EmailField(widget=forms.EmailInput, disabled=True)

	class Meta:
		model = Autore
		fields = ('username', 'password', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'active', 'admin')

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

	def clean_password(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Le passwords non corrispondono")
		return password

	def clean(self):
		self.clean_password()
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


	"""controllli da fare come script perche devo sapere quale utente e' loggato
	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Autore.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email gia' in uso")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = Autore.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username gia' in uso")
		return username
	"""

