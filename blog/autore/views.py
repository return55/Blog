from django.shortcuts import render, loader, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Autore


# Create your views here.

#Dovrebbe essere vuota, redirigo sul login
def index(request):
    return HttpResponseRedirect("1/") 

def info(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    #articoli = get_list_or_404(A)
    template = loader.get_template('autore/info.html')
    context = {
        'autore': autore,
    }
    return HttpResponse(template.render(context, request))

#da fare
def settings(request, id_autore):
    return HttpResponse("modifica info sull'autore " + (Autore.objects.get(pk=id_autore)).__str__())