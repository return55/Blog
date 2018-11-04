"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from autore.views import registrazione


urlpatterns = [
    path('', views.index, name='main'),
    path('admin/', admin.site.urls),
    path('autore/', include('autore.urls')),
    path('logout/', views.logout_view , name='logout'),
    path('articolo/', include('articolo.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('registrazione/', registrazione , name='registrazione'),
]

