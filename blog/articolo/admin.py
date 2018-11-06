from django.contrib import admin

from .forms import (
	ArticoloAdminChange,
) 
from .models import Articolo, Commento

class CommentoInline(admin.StackedInline):
    model = Commento
    extra = 1

class ArticoloAdmin(admin.ModelAdmin):
	form = ArticoloAdminChange
	
	fieldsets  = [
		(None,		  {'fields': ['titolo', 'id_autore', 'testo', 'categoria']}),
		('Opzionali', {'fields': ['keywords', 'citazioni']}),
	]
	inlines = [CommentoInline]
	list_display = ('titolo', 'data', 'get_nick_autore')
	list_filter = ['data']
	search_fields = ['testo']


class CommentoAdmin(admin.ModelAdmin):
	fields = ['id_articolo', 'testo', 'commentatore']

admin.site.register(Articolo, ArticoloAdmin)
admin.site.register(Commento, CommentoAdmin)
