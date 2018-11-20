from django.contrib import admin

from .forms import (
	ArticoloAdminChange, FormAdminCommento
) 
from .models import Articolo, Commento

class CommentoInline(admin.StackedInline):
	model = Commento
	form = FormAdminCommento
	extra = 1

class ArticoloAdmin(admin.ModelAdmin):
	form = ArticoloAdminChange
	
	fieldsets  = [
		(None,		  {'fields': ['titolo', 'id_autore', 'testo', 'categoria', 'data']}),
		('Opzionali', {'fields': ['keywords', 'cita']}),
	]
	inlines = [CommentoInline]
	
	list_display = ('titolo', 'data', 'get_nick_autore', 'citato', 'get_voto')
	list_filter = ['data', 'citato']
	search_fields = ('titolo', 'testo')

	def get_form(self, request, obj=None, **kwargs):
		if obj:
			#caso modifica
			self.readonly_fields = ['data', 'cita']
		else:
			#caso crea
			self.readonly_fields = ['data']
		return super().get_form(request, obj, **kwargs)


class CommentoAdmin(admin.ModelAdmin):
	form = FormAdminCommento
	
	fields = ['id_articolo', 'testo', 'commentatore']

	list_display = ('get_articolo_titolo', 'commentatore')
	list_filter = ['data']

admin.site.register(Articolo, ArticoloAdmin)
admin.site.register(Commento, CommentoAdmin)
