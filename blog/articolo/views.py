from django.shortcuts import render, loader, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse

from autore.models import Autore
from articolo.models import Articolo, Commento
from articolo.forms import (
    ArticoloAddForm, FormCommento
)


#mostra gli articoli piu' recenti
def index(request):
    ultimi_articoli = Articolo.objects.order_by('-data')[:10]
    autori = [Autore.objects.get(pk=art.id_autore.id) for art in ultimi_articoli]
    
    assert len(ultimi_articoli) == len(autori), "Articolo/index: numero articoli != numero autori"

    tutto = [(ultimi_articoli[i], autori[i]) for i in range(len(ultimi_articoli))]
    context = {
        'tutto' : tutto
    }
    return render(request, 'articolo/index.html' , context)

#mi fai vedere le info sull'articolo
def info(request, id_articolo):
    articolo = get_object_or_404(Articolo, pk=id_articolo)
    autore = articolo.id_autore
    try:
        commenti = Commento.objects.filter(id_articolo=id_articolo)
    except ObjectDoesNotExist:
        commenti = None
    template = loader.get_template('articolo/info.html')
    context = {
        'articolo' : articolo,
        'autore': autore,
        'commenti' : commenti,
        'citazioni' : articolo.cita.all()
    }
    return HttpResponse(template.render(context, request))

#Se l'utente e' autenticato -> commentatore = nick dell'utente
#Altrimenti -> commentatore = "Anonimo"
def aggiungi_commento(request, id_articolo):
    articolo = get_object_or_404(Articolo, pk=id_articolo)
    if request.method == 'POST':
        form = FormCommento(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.clean()
            if request.user.is_authenticated:
                commentatore = request.user.username
            else:
                commentatore = "Anonimo"
            nuovo_commento = Commento.objects.create(
                                id_articolo= articolo,
                                testo= data.get('testo'),
                                commentatore= commentatore
                            )
            nuovo_commento.save()
            messages.success(request, 'Commento creato correttamente')
            return redirect('articolo:info', permanent=True, id_articolo=id_articolo)
    else:
        form = FormCommento()

    return render(request, 'articolo/crea_commento.html', 
                    context={'form': form, 'articolo': articolo})


#mi fai vedere solo i commenti con il titolo dell'articolo, se richiesto
def commenti(request, id_articolo, titolo=False):
    #controllo se l'articolo esiste
    articolo = get_object_or_404(Articolo, pk=id_articolo) 
    try:
        commenti = Commento.objects.filter(id_articolo=id_articolo)
    except ObjectDoesNotExist:
        return render(request, 'articolo/no_comment.html', 
            {'titolo' : articolo.titolo, 'id_articolo' : id_articolo})
    #qui i commenti ci sono
    context = {
        'titolo' : articolo.titolo if titolo else '',
        'base' : "base.html",
        'commenti' : commenti,
        'id_articolo' : id_articolo,
    }
    return render(request, 'articolo/commenti.html', context=context)



#Mostro tutti gli articoli
def tutti(request):
    #aggiungi tutti gli articoli alla request
    context = None
    return render(request, 'articolo/tutti.html', context=context)

def cerca(request):
    return render(request, 'articolo/cerca.html')

def filtro_categoria(request, categoria):
    #controlla che la categoria sia valida
    return render(request, 'articolo/filtro_categoria.html', context={ 'categoria': categoria })