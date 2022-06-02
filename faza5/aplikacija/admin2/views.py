from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from igrac.models import *


"""Anja Kovačević 0484/19
Svakog dana se na osnovu jmbga provera kome je rođendan i dodeljuje mu se bonus
ukoliko jeste, takođe svaki dan se svim vip korisnicima smanjuje parametar vip za 1, a
kada dođe taj atribut do nule, korisnik prestaje da ima vip status.
"""
@login_required(login_url='index')
def bonusi(request):
    context={}
    if(request.user.pk==1):
        if (request.method=='POST'):
            danas = str(datetime.now())
            danas = "" + danas[8] + danas[9] + danas[5] + danas[6]
            """Nalaze se korisnici kojima je danas rođendan."""
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

"""
Nemanja Krivokapić 0588/19
Admin ima mogućnost da doda utakmicu koja će se odigrati u skorije vreme
"""
@login_required(login_url='index')
def dodajutakmicu(request):
    context = {}
    if (request.user.pk == 1):
        if(request.method=='POST'):
            form = DodavanjeUtakmiceForm(request.POST)
            if (form.is_valid()):
                """Prikupljaju se podaci iz forme i pravi se utakmica koja će biti u tom trenutku u najavi"""
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

"""Anja Kovačević 0484/19
Prikazuju se sve utakmice koje su u toku
"""
@login_required(login_url='index')
def prikaziaktivneutakmice(request):
    utakmicesve = ""
    utakmice = Utakmica.objects.all()

    utakmiceun=Utakmiceutoku.objects.all()

    for u in utakmice:
         for i in utakmiceun:
             """Nepohodno je da svaku utakmiceutoku nađemo u klasi uktamice kako bismo joj pokupili nephodne podatke"""
             if (i.pk ==u.pk):
                utakmicesve = utakmicesve + "Timovi:\t" + u.tim1 + " - " + u.tim2 + "\t\t\tDatum i vreme:\t" + u.datumpocetka + "" + "\n"

    context = {
        'utakmice': utakmicesve
    }
    return render(request, 'admin2/aktivneutakmice.html', context)

"""
Mihailo Milenković 0117/19
Nakon zavšene utakmice prolazi se kroz sve koji su odigrali deset u nizu,
ukoliko su dobili i broj pogodatak im je 10 ona postaju vip korisnici, a svim ostalim
se resetuje broj pogođenih
"""
@login_required(login_url='index')
def deset_u_nizu_rez(request, rezultat):
    tipovi = Desetunizu.objects.all()
    reset=0
    for tip in tipovi:
        if tip.validno:
            tip.validno = False
            if tip.odigrano == rezultat:
                tip.brojpogodaka += 1
            """Ukoliko je korisnik dosao do 10. pogotka"""
            if tip.brojpogodaka==10:
                korisnik=tip.idkor
                korisnik.vip=365
                if not korisnik.stanje:
                    korisnik.stanje=0
                korisnik.stanje+=1000
                korisnik.save()
                """Ukoliko postoji barem jedan korisnik kome je ovo 10. pogodak treba da se uradi reset"""
                reset=1
            else:
                tip.brojpogodaka = 0
            tip.save()
    """Resetovanje svih brojapogodaka od ostalih korisnika, ukoliko je neko došao do 10. pogotka"""
    if (reset == 1):
        for tips in tipovi:
            tips.brojpogodaka = 0
            tips.validno = False
            tips.save()
    return HttpResponse(tip) #todo neka povratna vrednost

"""
Mihailo Milenković 0117/19
Dodaje se nova utakmica za utakmicu na koju se korisnici klade u 10_u_nizu
"""
@login_required(login_url='index')
def dodajutakmicu10(request):
    if(request.method=='POST'):
        form = DodavanjeUtakmice10Form(request.POST)
        """Prikupljaju se podaci iz forme i pravi se utakmica na koju će korisnici da se klade u odeljku deset u nizu"""
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

"""Nemanja Krivokapić 0588/19
Utakmice koje su u najavi mogu da se startuju i prebacuju se u 
tabelu utakmiceutoku
"""
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
                    """Pokušava se dohvatanje utakmice sa datim atributima,
                    ukoliko ne postoji baca se greška
                    """
                    utakmica=Utakmica.objects.get(tim1=tim1, tim2=tim2, datumpocetka=datumvreme)

                except:
                    poruka = "Utakmica ne postoji!"
                    x=0

                if(x!=0):
                   """Pokušava se dohvatanje utakmice u najavi """
                   utakmicaun = Utakmiceunajavi.objects.filter(pk=utakmica)
                   if (len(utakmicaun)==0):
                       utakmicaun=utakmicaun[0]
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

"""
Nemanja Krivokapić 0588/19
Admin ima mogućnost da ugasi utakmicu i prebaci je u tabelu zavrsene utakmice,
zatim se u sve tiketdogadjaje  za tu utakmicu gleda šta je odigrano i ako je pogodak
upisuje se 1 u ishod, a 0 ukoliko je promašeno,
zatim se ažurira istorija utakmica gde se sada stavlja da je data utakmica završila. 
Vrši se isplaćivanje ukoliko su sa tiketa sve utakmice završene, ažurira se statistika,
i ukoliko se neko kladio na taj tiket koji je završen vrši se provera vip opklade i vrši se isplaćivanje

"""
@login_required(login_url='index')
def ugasiutakmicu(request):
    context = {}
    if (request.user.pk == 1):
        poruka = ""
        if(request.method=='POST'):
            poruka=""
            form=UgasiUtakmicuForm(request.POST)
            if form.is_valid():
                """Prikupljaju se podaci iz popunjene forme"""
                tim1 = form.cleaned_data['tim1']
                tim2 = form.cleaned_data['tim2']
                ishod = form.cleaned_data['ishod']
                ishod1=ishod
                datum=form.cleaned_data['datum']
                ishod=ishod.split(' ')
                utakmica= Utakmica.objects.filter(tim1=tim1, tim2=tim2, datumpocetka=datum)
                """Pokušava se pronalazak utakmice koja ima date atribute i ako je nađena, izbacuje se 
                iz utakmiceutoku i dodaje se u tabelu zavrsene utakmice
                """
                if(len(utakmica)!=0):
                    utakmica=utakmica[0]
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

                """U tiketdogadjaju se ažurira ishod ukoliko je korisnik pogodio"""
                tiketdogadjaj=Tiketdogadjaj.objects.filter(iduta=utakmica.iduta)
                for tiketd in tiketdogadjaj:
                    if(tiketd.odigrano==ishod[0] or tiketd.odigrano==ishod[1]  or tiketd.odigrano==ishod[2]  ):
                        tiketd.ishod=1
                    else:
                        tiketd.ishod=0
                    tiketd.save()
                    t=tiketd.idtik
                    t=Korisnik.objects.get(pk=t.idkor.idkor.idkor)

                    """Vrši se upis u istoirjuutakmica za sve one koji su se kladili na tu utakmicu"""
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
                    """Proverava se da li su sve utakmice sa datog tiketa gotove"""
                    tiketdog=Tiketdogadjaj.objects.filter(idtik=tiket)
                    dobijeno=1
                    for t in tiketdog:
                        if(t.ishod==0):
                            dobijeno=0
                        if(t.ishod==-1):
                            dobijeno=-1
                    if(dobijeno==1):
                        """Ukoliko je tiket dobijen, proverava se da lu se neko kladio na ovaj tiket"""

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
                        """Ažurira se statistika i brišu se svi tiketdogadjaji za tu utakmicu"""
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
                        """Ukoliko je tiket gubitan, proverava se da lu se neko kladio na ovaj tiket"""
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
                        """Ažurira se statisika i brušu se svi tikedogadjaji za datu utakmicu"""
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





