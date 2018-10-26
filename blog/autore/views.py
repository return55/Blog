from django.shortcuts import render, loader, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


from .models import Autore
from articolo.models import Articolo


# Create your views here.

#Dovrebbe essere vuota, redirigo sul login
def index(request):
    return HttpResponseRedirect("2/") 

#Mostro le info sull'autore e i link agli articoli
def info(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    articoli = Articolo.objects.filter(id_autore=id_autore)
    template = loader.get_template('autore/info.html')
    context = {
        'autore': autore,
        'articoli': articoli,
    }
    return HttpResponse(template.render(context, request))

#da fare
def settings(request, id_autore):
    return HttpResponse("modifica info sull'autore " + Autore.objects.get(pk=id_autore).__str__())

#mi manda sul form, poi da li vado in autore/aggiungi
def scrivi(request, id_autore, messaggio=""):
    categorie = Articolo.CATEGORIE_DISPONIBILI
    context = {
        'id_autore' : id_autore,
        'categorie' : categorie,
        'messaggio': messaggio,
    }
    return render(request, 'autore/crea_articolo.html', context=context)


def aggiungi_articolo(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    if request.method == 'POST':
        #controlli (da spostare su javascript)
        if request.POST['titolo'] == "":
            return HttpResponseRedirect(reverse('autore:scrivi', 
                args=(id_autore, "Il titolo non puo' essere vuoto")))
        if request.POST['testo'] == "":
            return HttpResponseRedirect(reverse('autore:scrivi',
                args=(id_autore, "Il testo non puo' essere vuoto")))
        #aggiungi un controlo sul radio button

        articolo = Articolo.objects.create(titolo=request.POST['titolo'],
            id_autore=autore,
            testo=request.POST['testo'],
            categoria=request.POST['categoria'])

        return HttpResponse("L'articolo e' stato creato")
    
        
