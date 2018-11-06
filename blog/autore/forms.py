from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Autore
from articolo.models import Commento


class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)

	class Meta:
		model = Autore
		fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'admin')

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

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Le passwords non corrispondono")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Autore
		fields = ('username', 'password', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico', 'active', 'admin')

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

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

class RegistrationForm(forms.ModelForm):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput)
	first_name = forms.CharField(label='Nome',max_length=20)
	last_name = forms.CharField(label='Cognome',max_length=20)
	bio = forms.CharField(label='Biografia',widget=forms.Textarea, required=False)
	profilo_pubblico = forms.BooleanField(required=False)

	#forse i 2 clean non servono
	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = Autore.objects.filter(username='username')
		if qs.exists():
			raise forms.ValidationError("Username gia' in uso")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Autore.objects.filter(email='email')
		if qs.exists():
			raise forms.ValidationError("Email gia' presente")
		return email

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Le passwords non corrispondono")
		return data

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
	
	class Meta:
		model = Autore
		fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico')

class SettingsForm(forms.ModelForm):
	username = forms.CharField(max_length=20)
	email = forms.EmailField(widget=forms.EmailInput)
	first_name = forms.CharField(label='Nome',max_length=20)
	last_name = forms.CharField(label='Cognome',max_length=20)
	bio = forms.CharField(label='Biografia',widget=forms.Textarea, required=False)
	profilo_pubblico = forms.BooleanField(required=False)

	class Meta:
		model = Autore
		fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profilo_pubblico')
	"""controllli da fare come script
	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Autore.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email gia' in uso")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = Autore.objects.filter(username='username')
		if qs.exists():
			raise forms.ValidationError("Username gia' in uso")
		return username
	"""

