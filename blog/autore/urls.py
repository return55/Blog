from django.urls import path, include
from . import views

app_name = 'autore'

urlpatterns = [
    path('', views.index, name='index'), #redirige su login (non ancora)
    path('<int:id_autore>/', views.info, name='info'),
    path('<int:id_autore>/settings/', views.settings, name='modifica_info'),
    path('<int:id_autore>/scrivi/', views.scrivi, name='scrivi'),
    path('<int:id_autore>/aggiungi_articolo/', views.aggiungi_articolo, name='aggiungi_articolo'),

]