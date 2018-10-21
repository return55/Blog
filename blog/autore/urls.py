from django.urls import path, include
from . import views

app_name = 'autore'

urlpatterns = [
    path('', views.index, name='index'), #redirige su login (non ancora)
    path('<int:id_autore>/', views.info, name='info_autore'),
    path('<int:id_autore>/settings/', views.settings, name='modifica_info_autore'),
    path('<int:id_autore>/scrivi/', views.scrivi, name='scrivi_articolo'),
    path('<int:id_autore>/aggiungi/', views.aggiungi, name='aggiungi_articolo'),

]