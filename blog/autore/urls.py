from django.urls import path, include
from django.contrib.auth.views import LoginView

from . import views

app_name = 'autore'

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html')),
    path('<int:id_autore>/', views.info, name='info'),
    path('<int:id_autore>/settings/', views.settings, name='settings'),
    path('<int:id_autore>/cambia_password/', views.cambia_password, name='cambia_password'),
    path('<int:id_autore>/aggiungi_articolo/', views.aggiungi_articolo, name='aggiungi_articolo'),
    path('tutti/', views.tutti, name='tutti'),
    path('cerca/', views.cerca, name='cerca'),
]