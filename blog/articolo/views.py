from django.shortcuts import render, loader, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from autore.models import Autore
from articolo.models import Articolo, Commento
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormCommento_ConNick, FormCommento_NoNick
from django.contrib import messages
from django.urls import reverse




# Create your views here.
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
        commenti = Commento.objects.get(id_articolo=id_articolo)
    except ObjectDoesNotExist:
        commenti = None
    template = loader.get_template('articolo/info.html')
    context = {
        'articolo' : articolo,
        'autore': autore,
        'commenti' : commenti,
    }
    return HttpResponse(template.render(context, request))

#mi fai vedere solo i commenti con il titolo dell'articolo, se richiesto
def commenti(request, id_articolo, titolo=False):
    #controllo se l'articolo esiste
    articolo = get_object_or_404(Articolo, pk=id_articolo) 
    try:
        commenti = Commento.objects.get(id_articolo=id_articolo)
    except ObjectDoesNotExist:
        return render(request, 'articolo/no_comment.html', {'titolo' : articolo.titolo})
    #qui i commenti ci sono
    context = {
        'titolo' : articolo.titolo if titolo else '',
        'commenti' : commenti,
    }
    return render(request, 'articolo/commenti.html', context=context)

#Se l'utente e' autenticato setto il nick qui e gli mostro un form senza nick.
#Altrimenti gli mostro il form col nick
def aggiungi_commento(request, id_articolo):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'articolo/crea_commento.html', { 'form': FormCommento_ConNick(initial={'nick': 1}),})         
        else:
            return render(request, 'articolo/crea_commento.html', { 'form': FormCommento_ConNick(),})
    else:
        if request.user.is_authenticated():
            c = FormCommento_NoNick(request.POST)
        else:
            c = FormCommento_ConNick(request.POST)
        #controlla perche' il form non funziona
        if c.is_valid():
            
            nuovo_comm = c.save()
            messages.success(request, 'Commento creato correttamente')
            return HttpResponseRedirect(reverse('articolo:info', args=(id_articolo)))
        else:

            return HttpResponse(c.errors.as_text())



