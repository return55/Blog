from django.shortcuts import render, loader, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Autore
from articolo.models import Articolo
from .forms import  (
    FormCommento_ConNick, FormCommento_NoNick, 
    UserAdminChangeForm,  
     RegistrationForm,
)


#Mostro le info sull'autore e i link agli articoli
def info(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    if request.user.id == autore.id or autore.profilo_pubblico :
        articoli = Articolo.objects.filter(id_autore=id_autore)
        template = loader.get_template('autore/info.html')
        context = {
            'autore': autore,
            'articoli': articoli,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("Non puoi accedere alle informazioni personali di ", autore.__str__())

#da fare
@login_required()
def settings(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    if request.user.id == autore.user.id:
        if request.method == "POST":
            form = UserAdminChangeForm(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return reverse('autore:info', args=(id_autore,))                
        else:
            user = request.user
            profile = user.profile
            form = UserAdminChangeForm(instance=profile)
            return render(request, "autore/settings.html", { 'form': form, 'id_autore': id_autore})
    else:
        return HttpResponse("Non puoi modificare le informazioni personali di ", autore.__str__())

@login_required()
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
    else:
        categorie = Articolo.CATEGORIE_DISPONIBILI
        context = {
            'id_autore' : id_autore,
            'categorie' : categorie,
        }
        return render(request, 'autore/crea_articolo.html', context=context)

#Se l'utente e' autenticato setto il nick qui e gli mostro un form senza nick.
#Altrimenti gli mostro il form col nick
def aggiungi_commento(request, id_articolo):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'articolo/crea_commento.html', { 'form': FormCommento_NoNick(),})         
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
            return HttpResponseRedirect(reverse('articolo:info', args=(id_articolo,)))
        else:
            return HttpResponse(c.errors.as_text())

def registrazione(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            nuovo_utente = form.save()
            # redirect to a new URL:
            messages.info(request, 'Grazie per la registrazione')
            nuovo_utente = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, nuovo_utente)
            #calcola id autore
            return redirect('autore:info', permanent=True, id_autore=Autore.objects.get(username=form.cleaned_data.get('username')).id)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()
        return render(request, 'autore/registrazione.html', context={'form': form})

#mostro tutti gli atori col profilo pubblico: nome, cognome che e' un link alla loro pagina
#se riesco li rendo ordinabili per data iscrizione e ricerca per nome e cognome
def tutti(request):
    autori = Autore.objects.filter(profilo_pubblico=True)
    if autori != None :
        context = {
            'autori' : autori,
            'tutti' : True,
        }
        return render(request, 'autore/risultati_ricerca.html', context=context)
    else:
       messages.info(request, 'Purtroppo non ci sono autori con profili pubblici')
       return render(request, 'autore/risultati_ricerca.html')

#creo un form apposta e lo mando (get) al ritorno analizzo i risultati (post)
def cerca(request):
    return render(request, 'autore/cerca.html', context={})



    
        
