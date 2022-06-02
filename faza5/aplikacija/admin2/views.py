from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from igrac.models import *

@login_required(login_url='index')
def bonusi(request):
    context={}
    if(request.user.pk==1):
        if (request.method=='POST'):
            danas = str(datetime.now())
            danas = "" + danas[8] + danas[9] + danas[5] + danas[6]
            korisnici = Korisnik.objects.filter(jmbg__startswith=danas)
            for k in korisnici:
                korisnik=Korisnik.objects.get(pk=k.pk)
                if(korisnik.vip):
                    korisnik.stanje=korisnik.stanje+2500
                else:
                    korisnik.stanje = korisnik.stanje + 1000
                korisnik.save()
        context={}
        return render(request, 'admin2/bonusi.html', context)
    return render(request, 'registracija/greska.html', context)

@login_required(login_url='index')
def dodajutakmicu(request):
    context = {}
    if (request.user.pk == 1):
        if(request.method=='POST'):
            form = DodavanjeUtakmiceForm(request.POST)
            if (form.is_valid()):
                tim1=form.cleaned_data['tim1']
                tim2 = form.cleaned_data['tim2']
                datumvreme = form.cleaned_data['datumvreme']
                d=str(datumvreme)
                utakmica=Utakmica()
                utakmica.tim1=tim1
                utakmica.tim2 = tim2
                utakmica.datumpocetka = d
                utakmica.pk=Utakmica.objects.count()+1
                utakmica2=Utakmiceunajavi()
                utakmica2.pk=utakmica.pk
                utakmica.save()
                utakmica2.save()


        form=DodavanjeUtakmiceForm()
        context={'form': form}
        return render(request, 'admin2/postaviutakmicu.html', context)
    return render(request, 'registracija/greska.html', context)
@login_required(login_url='index')
def deset_u_nizu_rez(request, rezultat):
    tipovi = Desetunizu.objects.all()
    for tip in tipovi:
        if tip.validno:
            tip.validno = False
            if tip.odigrano == rezultat:
                tip.brojpogodaka += 1
            else:
                tip.brojpogodaka = 0
            tip.save()
    return HttpResponse(tip) #todo neka povratna vrednost

@login_required(login_url='index')
def dodajutakmicu10(request):
    if(request.method=='POST'):
        form = DodavanjeUtakmice10Form(request.POST)
        if (form.is_valid()):
            tim1=form.cleaned_data['tim1']
            tim2 = form.cleaned_data['tim2']
            if(tim1 and tim2):
                ut = "" + tim1 + " - " + tim2
                utakmica = Utakmica10.objects.all()
                if(len(utakmica)==0):
                    utakmica=Utakmica10()
                    utakmica.utakmica10=ut
                else:
                    utakmica[0].delete()
                    utakmica = Utakmica10()
                    utakmica.utakmica10 = ut
                utakmica.save()

    form=DodavanjeUtakmice10Form()
    context={'form': form}
    return render(request, 'admin2/postaviutakmicu10.html', context)

@login_required(login_url='index')
def prikaziaktivneutakmice(request):
    utakmicesve = ""
    utakmice = Utakmica.objects.all()

    utakmiceun=Utakmiceutoku.objects.all()

    for u in utakmice:
         for i in utakmiceun:
             if (i.pk ==u.pk):
                utakmicesve = utakmicesve + "Timovi:\t" + u.tim1 + " - " + u.tim2 + "\t\t\tDatum i vreme:\t" + u.datumpocetka + "" + "\n"

    context = {
        'utakmice': utakmicesve
    }
    return render(request, 'admin2/aktivneutakmice.html', context)

@login_required(login_url='index')
def ugasiutakmicu(request):
    context = {}
    if (request.user.pk == 1):
        poruka = ""
        if(request.method=='POST'):
            poruka=""
            form=UgasiUtakmicuForm(request.POST)
            if form.is_valid():
                tim1 = form.cleaned_data['tim1']
                tim2 = form.cleaned_data['tim2']
                ishod = form.cleaned_data['ishod']
                ishod1=ishod
                datum=form.cleaned_data['datum']
                ishod=ishod.split(' ')
                utakmica= Utakmica.objects.get(tim1=tim1, tim2=tim2, datumpocetka=datum)
                if(utakmica):
                    zabrisanje=Utakmiceutoku.objects.get(pk=utakmica.pk)
                    zavrsena = Zavrseneutakmice()
                    zavrsena.iduta=utakmica
                    zavrsena.ishod=ishod[0]
                    zavrsena.poluvremekraj=ishod[1]
                    zavrsena.prvigol=ishod[2]
                    zavrsena.save()
                    zabrisanje.delete()
                    poruka="Uspesno ste obrisali utakmicu!"
                else:
                    prouka="Utakmica ne postoji!"
                    form = UgasiUtakmicuForm()
                    context = {'form': form, 'poruka': poruka}
                    return render(request, 'admin2/ugasiutakmicu.html', context)

                #isplacivanje!!!!
                tiketdogadjaj=Tiketdogadjaj.objects.filter(iduta=utakmica.iduta)
                for tiketd in tiketdogadjaj:
                    if(tiketd.odigrano==ishod[0] or tiketd.odigrano==ishod[1]  or tiketd.odigrano==ishod[2]  ):
                        tiketd.ishod=1
                    else:
                        tiketd.ishod=0
                    tiketd.save()
                    t=tiketd.idtik
                    t=Korisnik.objects.get(pk=t.idkor.idkor.idkor)
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    s=tim1+" : "+tim2+" "+tiketd.odigrano
                    ist=Istorijautakmica.objects.filter(odigrano=s)
                    ist.delete()
                    kraj = "Datum: " + datum + "    |   " + tim1 + " : " + tim2 + "    |   Ishod: " + ishod1
                    istorija = Istorijautakmica()
                    istorija.ishod = tiketd.ishod
                    istorija.idkor = t
                    istorija.odigrano =  kraj

                    istorija.save()

                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                tiketi=Tiket.objects.all()
                for tiket in tiketi:

                    tiketdog=Tiketdogadjaj.objects.filter(idtik=tiket)
                    dobijeno=1
                    for t in tiketdog:
                        if(t.ishod==0):
                            dobijeno=0
                        if(t.ishod==-1):
                            dobijeno=-1
                    if(dobijeno==1):

                        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        try:
                            viptiket=Viptiket.objects.get(idtik=tiket)
                            if(viptiket.odigrano=='Prolaz'):
                                k=Korisnik.objects.get(pk=viptiket.idkvo.pk)
                                i=Korisnik.objects.get(pk=viptiket.idkor.pk)
                                i.stanje+=viptiket.dobitak
                                k.stanje-=viptiket.dobitak
                                i.save()
                                k.save()
                            viptiket.delete()
                            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        except:
                            dalje=1
                        for t in tiketdog:
                            t.delete()
                        s=tiket.idkor.pk
                        korisnik=Korisnik.objects.get(pk=s)
                        dob=tiket.iznosuplate*tiket.kvota
                        korisnik.stanje=korisnik.stanje+dob
                        #dodati korisniku statistiku
                        korisnik.save()

                        # povecati broj dobijenih kvoteru ili broj izgubljenih
                        s=tiket.idkvo.idkor.pk
                        kvoter = Korisnik.objects.get(pk=s)
                        kvoter.stanje = kvoter.stanje - tiket.iznosuplate * tiket.kvota

                        statistika = Statistika.objects.get(idkor=s)
                        statistika.brojprimljenihpogodjenih = statistika.brojprimljenihpogodjenih + 1
                        kvoter.save()
                        statistika.save()

                        statistika=Statistika.objects.get(idkor=tiket.idkor.pk)
                        statistika.brojpogodjenih = statistika.brojpogodjenih + 1
                        statistika.ukupnodobijeno=statistika.ukupnodobijeno+dob
                        statistika.ukupnouplaceno=statistika.ukupnouplaceno+tiket.iznosuplate
                        statistika.save()

                        tiket.delete()
                    if(dobijeno==0):

                        try:
                            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                            viptiket = Viptiket.objects.get(idtik=tiket)
                            if (viptiket.odigrano == 'Pad'):
                                k = Korisnik.objects.get(pk=viptiket.idkvo.pk)
                                i = Korisnik.objects.get(pk=viptiket.idkor.pk)
                                i.stanje += viptiket.dobitak
                                k.stanje -= viptiket.dobitak
                                i.save()
                                k.save()
                            viptiket.delete()
                            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        except:
                            dalje=1
                        for t in tiketdog:
                            t.delete()

                        statistika = Statistika.objects.get(idkor=tiket.idkor.idkor)
                        statistika.ukupnouplaceno = statistika.ukupnouplaceno + tiket.iznosuplate
                        statistika.brojpromasenih=statistika.brojpromasenih+1
                        statistika.save()

                        statistika = Statistika.objects.get(idkor=tiket.idkvo.idkor)
                        statistika.brojprimljenihpromasenih = statistika.brojprimljenihpromasenih + 1

                        statistika.save()
                        tiket.delete()
                """postavljeneKvote=Postavljenekvote.objects.get(iduta=utakmica)
                for p in postavljeneKvote:
                    p.delete()""" #TODO Obrisati komentar kada se bude ispravilo u bazi da u postavljene kvote su Utakmica
                                 #TODO a ne UtakmicaUNajavi


        form=UgasiUtakmicuForm()
        context={ 'form' : form, 'poruka': poruka}
        return render(request, 'admin2/ugasiutakmicu.html', context)
    return render(request, 'registracija/greska.html', context)
@login_required(login_url='index')
def startujutakmicu(request):

    poruka=''
    x=1
    form = StartujUtakmicuForm()
    context = {}
    if (request.user.pk == 1):
        if(request.method=='POST'):
            form=StartujUtakmicuForm(request.POST)
            if form.is_valid():
                tim1 = form.cleaned_data['tim1']
                tim2 = form.cleaned_data['tim2']
                datumvreme = form.cleaned_data['datum']
                try:

                    utakmica=Utakmica.objects.get(tim1=tim1, tim2=tim2, datumpocetka=datumvreme)

                except:
                    poruka = "Utakmica ne postoji!"
                    x=0

                if(x!=0):
                   utakmicaun = Utakmiceunajavi.objects.get(pk=utakmica)
                   if (utakmicaun):
                       utakmicaun.delete()
                       u = Utakmiceutoku()
                       u.pk = utakmica.iduta
                       u.save()
                       poruka = "Uspesno ste startovali utakmicu"
                   else:
                       poruka = "Utakmica ne postoji!"

        context={
            'form': form,
            'poruka': poruka
        }
        return render(request, 'admin2/startujutakmicu.html', context)
    return render(request, 'registracija/greska.html', context)