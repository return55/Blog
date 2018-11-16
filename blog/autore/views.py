from django.shortcuts import render, loader, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import re

from .models import Autore
from articolo.models import Articolo, Commento
from .forms import  (
    UserAdminChangeForm,  SettingsForm,
    RegistrationForm, CercaAutoreForm
)
from articolo.forms import (
    ArticoloAddForm, FormCommento
)


#Mostro le info sull'autore e i link agli articoli
#finito
def info(request, id_autore):
    if request.user.is_authenticated:
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
    else:
        messages.info(request, "Prima devi effettuare il login")
        return HttpResponseRedirect(reverse('login')) 


@login_required()
def settings(request, id_autore):
    autore = get_object_or_404(Autore, pk=id_autore)
    if request.user.id != autore.id:
        messages.error(request, 'Non puoi modificare le informazioni personali di ' + autore.__str__())
        return HttpResponseRedirect(reverse('main'))
    else:
        if request.method == "POST":
            form = SettingsForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('autore:info', args=(id_autore,)))
        else:
            #per la get creo un form pulito
            user = request.user
            form = SettingsForm(instance=user)        
        return render(request, "autore/settings.html", { 'form': form, 'id_autore': id_autore})

def registrazione(request):
    form = RegistrationForm()
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
    else:
        #alla get do un form pulito
        form = RegistrationForm()
    
    return render(request, 'autore/registrazione.html', context={'form': form})
    
#finito
@login_required()
def cambia_password(request, id_autore):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password cambiata con successo')
            return HttpResponseRedirect(reverse('autore:info', args=(id_autore,)))
        else:
            messages.error(request, 'Non posso salvare, e\' presente un errore')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'autore/cambia_password.html', {
        'form': form
    })       

@login_required()
def aggiungi_articolo(request, id_autore):
    categorie = Articolo.CATEGORIE_DISPONIBILI
    context = {
        'categorie' : categorie,
    }
    if request.method == 'POST':
        form = ArticoloAddForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.clean()
            nuovo_articolo = Articolo.objects.create(
                                titolo= data.get('titolo'),
                                id_autore= request.user,
                                testo= data.get('testo'),
                                keywords= data.get('keywords'),
                                categoria= data.get('categoria')
                            )
            for arti in data.get('cita'):
                nuovo_articolo.cita.add(arti)
            nuovo_articolo.save()
            messages.success(request, 'Articolo creato correttamente.')
            return redirect('articolo:info', permanent=True, id_articolo=nuovo_articolo.id)
    else:
        form = ArticoloAddForm()

    context['form']= form
    
    return render(request, 'autore/crea_articolo.html', context=context)

#mostro tutti gli autori, quelli col profilo pubblico saranno dei link.
#mostro: nome, cognome, username
#se riesco li rendo ordinabili per data iscrizione e ricerca per nome e cognome
def tutti(request):
    autori = Autore.objects.all()
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
    if request.method == "POST":
        form = CercaAutoreForm(request.POST)
        if form.is_valid():
            data = form.clean()
            autori_risultati = Autore.objects.filter(profilo_pubblico=True)
            for campo, val in data.items():
                print(campo, "-", val, "-", sep=''  )
                if val != None and val != '' and re.match(r'data.*', campo) is None :
                    cmd = "autori_risultati.filter("+campo.__str__()+"=val)"
                    autori_risultati = eval(cmd)
            #controllo la data
            data_inizio = data.get('data_inizio')
            data_fine = data.get('data_fine')
            if data_inizio != None and data_fine != None:
                #ricerca range
                cmd = "autori_risultati.filter(data_registrazione__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                autori_risultati = eval(cmd)
            elif data_inizio != None:
                #ricerca  [data inizio - oggi]
                data_fine = datetime.date.today()
                print(data_fine)
                cmd = "autori_risultati.filter(data_registrazione__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                autori_risultati = eval(cmd)
            elif data_fine != None:
                #ricerca [oggi - data fine]
                data_inizio = datetime.date.today()
                print(data_inizio)
                cmd = "autori_risultati.filter(data_registrazione__range=[\""+data_inizio.__str__()+"\", \""+data_fine.__str__()+"\"])"
                autori_risultati = eval(cmd)

            return render(request, 'autore/risultati_ricerca.html', context={'autori': autori_risultati.all()})
    else:
        form = CercaAutoreForm()       
    return render(request, 'autore/cerca.html', { 'form': form })



    
        
