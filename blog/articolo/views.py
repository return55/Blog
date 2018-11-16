from django.shortcuts import render, loader, get_object_or_404, get_list_or_404, redirect
from django.http import (
    HttpResponse, HttpResponseRedirect,
    HttpResponseNotFound, HttpResponseNotAllowed
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector
)
import re
import datetime

from autore.models import Autore
from articolo.models import Articolo, Commento
from articolo.forms import (
    ArticoloAddForm, FormCommento,
    CercaArticoloForm
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
    articoli = Articolo.objects.all()
    if articoli != None :
        context = {
            'articoli' : articoli,
            'tutti' : True,
        }
        return render(request, 'articolo/risultati_ricerca.html', context=context)
    else:
       messages.info(request, 'Al momento non sono presenti articoli')
       return render(request, 'articolo/risultati_ricerca.html')

#creo un form apposta e lo mando (get) al ritorno analizzo i risultati (post)
#ho messo i controlli sul testo e sul titolo alla fine cosi' da non perdere
#il ranking.
def cerca(request):
    if request.method == "POST":
        form = CercaArticoloForm(request.POST)
        if form.is_valid():
            data = form.clean()
            articoli_risultati = Articolo.objects.all()

            #cerco su id_autore
            if data.get('id_autore') != None:
                articoli_risultati = articoli_risultati.filter(id_autore=data.get('id_autore'))
    
            #cerco su categoria
            if data.get('categoria') != '':
                articoli_risultati = articoli_risultati.filter(categoria=data.get('categoria'))

            #cerco su tutte le keywords
            keywords = data.get('keywords')
            if len(keywords) != 0:
                articoli_risultati = articoli_risultati.filter(keywords__contains=keywords)

            #controllo la data
            data_inizio = data.get('data_inizio')
            data_fine = data.get('data_fine')
            if data_inizio != None and data_fine != None:
                #ricerca range
                cmd = "articoli_risultati.filter(data__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                articoli_risultati = eval(cmd)
            elif data_inizio != None:
                #ricerca  [data inizio - oggi]
                data_fine = datetime.date.today()
                cmd = "articoli_risultati.filter(data__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                articoli_risultati = eval(cmd)
            elif data_fine != None:
                #ricerca [oggi - data fine]
                data_inizio = datetime.date(2017, 1, 1)
                cmd = "articoli_risultati.filter(data__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                articoli_risultati = eval(cmd)

            #controllo citato
            if data.get('citato') != None:
                articoli_risultati = articoli_risultati.filter(citato__gte=data.get('citato'))

            #ordino gli articoli rimasti in base alle parole
            #limito il numero dei risultati a 15 quando ranko
            parole = data.get('parole')
            print(parole)
            if parole != '':
                parole = parole.__str__().split()
                #creo il vettore: campo in cui cercare
                vector = SearchVector('testo', 'titolo')
                #creo la query
                query = ""
                for parola in parole:
                    print(parola)
                    query = query + "SearchQuery('"+parola+"') & "
                query = eval(query[:len(query)-2])
                print(query)
                #cerco
                articoli_risultati = articoli_risultati.annotate(rank=SearchRank(vector, query)).order_by('-rank')
                return render(request, 'articolo/risultati_ricerca.html', context={'articoli': articoli_risultati.all()[:15]})
            

            return render(request, 'articolo/risultati_ricerca.html', context={'articoli': articoli_risultati.all()})
    else:
        form = CercaArticoloForm()       
    return render(request, 'articolo/cerca.html', { 'form': form })


def filtro_categoria(request, categoria):
    context={ 
        'categoria': categoria,
        'articoli': Articolo.objects.filter(categoria=categoria)
    }
    return render(request, 'articolo/filtro_categoria.html', context=context)

def chi_mi_cita(request, id_articolo):
    articolo = get_object_or_404(Articolo, pk=id_articolo)
    context = {
        'titolo': articolo.titolo,
        'articoli': Articolo.objects.filter(cita=articolo.id)
    }
    print(Articolo.objects.filter(cita=articolo.id))
    return render(request, 'articolo/chi_mi_cita.html', context=context)

#puoi votare solo se:
#-sei autenticato
#-l'articolo non e' stato scitto da te
#-non hai gia' votato questo articolo.
#Una richiesta get porta a una pagina di errore.
@login_required()
def vota(request, id_articolo):
    articolo = get_object_or_404(Articolo, pk=id_articolo)
    if request.method == 'POST':
        #controllo che l'articolo non sia dell'utente autenticato
        articoli_utente = Articolo.objects.filter(id_autore=request.user.id)
        if articolo.id in [ articolo.id for articolo in articoli_utente ]:
            return render(request, 'articolo/messaggi_votazione.html', context={'titolo': "Non puoi votare un tuo articolo !!"})
        #controllo che non sia gia' stato votato
        articoli_votati = request.user.articoli_votati
        if articolo.id in articoli_votati:
            return render(request, 'articolo/messaggi_votazione.html', context={'titolo': "Non puoi votare lo stesso articolo 2 volte !!"})
        #fine dei controlli
        voto = int(request.POST['voto'])
        print(voto)

        request.user.articoli_votati.append(articolo.id)
        articolo.somma_voti += voto
        articolo.numero_voti += 1

        request.user.save()
        articolo.save()

        messages.success(request, 'Votazione avvenuta con successo.')
        return HttpResponseRedirect(reverse('articolo:info', args=(id_articolo,)))        
    else:
        #con la get restituisco una pagina di errore
        return render(request, 'articolo/messaggi_votazione.html', context={'titolo': "Per votare un articolo devi andare nella sua pagina delle informazioni."})
