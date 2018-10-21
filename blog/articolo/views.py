from django.shortcuts import render, loader, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from autore.models import Autore
from articolo.models import Articolo

# Create your views here.
#mostra gli articoli piu' recenti
def index(request):
    ultimi_articoli = Articolo.objects.order_by('-data')[:10]
    autori = [Autore.objects.get(pk=art.id_autore.id) for art in ultimi_articoli]
    
    assert len(ultimi_articoli) == len(autori), "Articolo/inex: numero articoli != numero autori"

    tutto = [(ultimi_articoli[i], autori[i]) for i in range(len(ultimi_articoli))]
    context = {
        'tutto' : tutto
    }
    return render(request, 'articolo/index.html' , context)

#mi fai vedere le info sull'articolo
def info(request):
    return render(request, 'articolo/info.html', {})

#mi fai vedere solo i commenti
def commenti(request):
    return render(request, 'articolo/commenti.html', {})
