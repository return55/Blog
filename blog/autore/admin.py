from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import  UserAdminChangeForm, RegisterForm
from .models import Autore

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = RegisterForm

	fieldsets = [
		(None, {'fields': ('username', 'password')}),
        ('Personal Info',{'fields': ('first_name', 'last_name', 'email')}),
		('Altre', {'fields': ['bio', 'profilo_pubblico', 'data_registrazione']}),
        ('Permissions', {'fields': ('is_admin',)}),
	]
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'admin')}),
    )
	readonly_fields = ['data_registrazione', 'is_admin']
	list_filter = ['data_registrazione']
	list_display = ('username', 'data_registrazione', 'profilo_pubblico')
	search_fields = ('username',)
	ordering = ('data_registrazione', 'first_name')
	filter_horizontal = ()
	verbose_name_plural = 'Autori'

admin.site.register(Autore, UserAdmin)

# Remove Group Model from admin.
admin.site.unregister(Group)
