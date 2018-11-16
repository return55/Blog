from django.urls import path, include
from . import views
from .models import Articolo

app_name = 'articolo'

urlpatterns = [
    path('', views.index, name='index'), #e' la main
    path('<int:id_articolo>/', views.info, name='info'),
    path('<int:id_articolo>/nuovo_commento/', views.aggiungi_commento, name='aggiungi_commento'),
    path('<int:id_articolo>/commenti/', views.commenti, {'titolo': True}, name='commenti' ),
    path('tutti/', views.tutti, name='tutti'),
    path('cerca/', views.cerca, name='cerca'),
    path('filtro_categoria/<str:categoria>', views.filtro_categoria, name='filtro_categoria'),
    path('<int:id_articolo>/chi_mi_cita/', views.chi_mi_cita, name='chi_mi_cita'),
    path('<int:id_articolo>/vota/', views.vota, name='vota'),
]