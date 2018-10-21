from django.urls import path, include
from . import views

app_name = 'articolo'

urlpatterns = [
    path('', views.index, name='index'), #e' la main
    path('<int:id_articolo>/', views.info, name='info_articolo'),
    path('<int:id_articolo>/commenti/', views.commenti, name='commenti_articolo'),
    

]