from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

#finita
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
    return HttpResponseRedirect(reverse('articolo:index'))

def login(request):
   return render(request, 'login.html')
