from django.shortcuts import render, loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Autore


# Create your views here.

#Dovrebbe essere vuota, redirigo sul login
def main(request):
    return HttpResponseRedirect("1/") 

def info(request, id_autore):
    autore = Autore.objects.get(pk=id_autore)
    template = loader.get_template('autore/info.html')
    context = {
        'autore': autore,
    }
    return HttpResponse(template.render(context, request))

def settings(request, id_autore):
    return HttpResponse("modifica info sull'autore " + (Autore.objects.get(pk=id_autore)).__str__())