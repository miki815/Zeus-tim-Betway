from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *


def bonusi(request):
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

def dodajutakmicu(request):
    x=1
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

def dodajutakmicu10(request):
    if(request.method=='POST'):
        form = DodavanjeUtakmice10Form(request.POST)
        if (form.is_valid()):
            tim1=form.cleaned_data['tim1']
            tim2 = form.cleaned_data['tim2']
            if(tim1 and tim2):
                ut = "" + tim1 + " - " + tim2
                utakmica = Utakmica10.objects.all()
                utakmica=utakmica[0]
                utakmica.utakmica10=ut
                utakmica.save()

    form=DodavanjeUtakmice10Form()
    context={'form': form}
    return render(request, 'admin2/postaviutakmicu10.html', context)

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

def ugasiutakmicu(request):
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
                    for t in tiketdog:
                        t.delete()
                    s=tiket.idkor.pk
                    korisnik=Korisnik.objects.get(pk=s)
                    korisnik.stanje=korisnik.stanje+tiket.iznosuplate*tiket.kvota
                    #dodati korisniku statistiku
                    korisnik.save()

                    tiket.delete()

                    # povecati broj dobijenih kvoteru ili broj izgubljenih
                    s=tiket.idkvo.idkor.pk
                    kvoter = Korisnik.objects.get(pk=s)
                    kvoter.stanje = kvoter.stanje - tiket.iznosuplate * tiket.kvota

                    statistika = Statistika.objects.get(idkor=s)
                    statistika.brojprimljenihpromasenih = statistika.brojprimljenihpromasenih + 1
                    kvoter.save()
                    statistika.save()
                    statistika=Statistika.objects.get(idkor=tiket.idkor.pk)
                    statistika.save()
                if(dobijeno==0):
                    for t in tiketdog:
                        t.delete()
                    tiket.delete()
                    statistika = Statistika.objects.get(idkor=tiket.idkor.idkor)
                    statistika.save()
                    statistika = Statistika.objects.get(idkor=tiket.idkvo.idkor)
                    statistika.brojprimljenihpromasenih = statistika.brojprimljenihpromasenih + 1
                    statistika.save()
            """postavljeneKvote=Postavljenekvote.objects.get(iduta=utakmica)
            for p in postavljeneKvote:
                p.delete()""" #TODO Obrisati komentar kada se bude ispravilo u bazi da u postavljene kvote su Utakmica
                             #TODO a ne UtakmicaUNajavi




    form=UgasiUtakmicuForm()
    context={ 'form' : form, 'poruka': poruka}
    return render(request, 'admin2/ugasiutakmicu.html', context)

def startujutakmicu(request):
    poruka=''
    x=1
    form = StartujUtakmicuForm()
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