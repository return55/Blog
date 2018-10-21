from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'), #redirige su login (non ancora)
    path('<int:id_autore>/', views.info, name='info_autore'),
    path('<int:id_autore>/settings', views.settings, name='modifica_info_autore'),

]