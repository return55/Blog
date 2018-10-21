from django.urls import path, include
from . import views
from .models import Articolo

app_name = 'articolo'

urlpatterns = [
    path('', views.index, name='index'), #e' la main
    path('<int:id_articolo>/', views.info, name='info'),
    path('<int:id_articolo>/commenti/', views.commenti, {'titolo': True}, name='commenti' ),
    path('<int:id_articolo>/nuovo_commento/', views.aggiungi_commento, name='aggiungi_commento'),

    

]