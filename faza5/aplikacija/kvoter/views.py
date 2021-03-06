from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from igrac.models import *

def index(request):
    return HttpResponse("Kvoter ovde")

"""Nemanja Krivokapić 0588/19
Pravljenje kvote za utakmice koje su u najavi
"""
@login_required(login_url='index')
def napravikvote(request, userId):
    context = {}
    if (request.user.pk == userId):
        poruka=""
        kvoter = Korisnik.objects.filter(idkor=userId)
        kvoter = list(kvoter)
        kvoter = kvoter[0]
        vip = 1 if kvoter.vip else 0
        if(request.method == 'POST'):
            form = KvoteForm(request.POST or None, request.FILES)
            if form.is_valid():
                """Uzimanje podataka iz forme koja je prethodno popunjena"""
                prviTim = form.cleaned_data['prviTim']
                drugiTim = form.cleaned_data['drugiTim']
                datum = form.cleaned_data['datum']
                try:
                    """Ukoliko takva utakmica ne postoji prijavljuje se greška."""
                    utakmica = Utakmica.objects.get(tim1=prviTim, tim2=drugiTim, datumpocetka=datum)
                except ObjectDoesNotExist:
                    utakmica=0
                    poruka="Utakmica ne postoji!"
                if(utakmica):
                    """Iz forme se prikupljaju podaci i pravi se klasa Postavljenekvote koje kvoter pravi i koje 
                    kasnije korisnici mogu da vide.
                    """
                    kec = form.cleaned_data['kec']
                    x = form.cleaned_data['x']
                    dvojka = form.cleaned_data['dvojka']
                    jj = form.cleaned_data['jj']
                    jx = form.cleaned_data['jx']
                    jd =form.cleaned_data['jd']
                    xj = form.cleaned_data['xj']
                    xx = form.cleaned_data['xx']
                    xd = form.cleaned_data['xd']
                    dj = form.cleaned_data['dj']
                    dx = form.cleaned_data['dx']
                    dd = form.cleaned_data['dd']
                    prvigol = form.cleaned_data['prvigol']
                    xgol = form.cleaned_data['xgol']
                    drugigol = form.cleaned_data['drugigol']
                    novakvota= Postavljenekvote()

                    novakvota.idkor=Kvoter.objects.get(pk=userId)
                    novakvota.kvota1=float(kec)
                    novakvota.kvotax= float(x)
                    novakvota.kvota2 = float(dvojka)

                    novakvota.kvota11 = float(jj)
                    novakvota.kvota1x = float(jx)
                    novakvota.kvota12 = float(jd)

                    novakvota.kvotax1 = float(xj)
                    novakvota.kvotaxx = float(xx)
                    novakvota.kvotax2 = float(xd)

                    novakvota.kvota21 = float(dj)
                    novakvota.kvota2x = float(dx)
                    novakvota.kvota22 = float(dd)

                    novakvota.prvigol1=float(prvigol)
                    novakvota.prvigol2 = float(xgol)
                    novakvota.prvigol3 = float(drugigol)
                    nadjeno=1
                    try:
                        un=Utakmiceunajavi.objects.get(pk=utakmica)
                    except:
                        nadjeno=0

                    if(nadjeno):
                        """Ukoliko je data utakmica počela prijavljuje se greška"""
                        novakvota.iduta=utakmica
                        novakvota.idkvo=Postavljenekvote.objects.count()+1
                        novakvota.save()
                        poruka="Uspesno ste dodali kvote!"
                    else:
                        poruka = "Utakmica je već počela!"

        #print(form.errors)
        form=KvoteForm()
        print(form.errors)
        context={'form': form, 'poruka': poruka, 'userId': userId, 'vip': vip}
        return render(request, 'kvoter/kvoter.html', context)
    return render(request, 'registracija/greska.html', context)

"""Anja Kovačević 0484/19
Ispisivanje svih utakmica u najavi na html stranicu Aktivne utakmice
"""
@login_required(login_url='index')
def prikaziaktivneutakmice(request, userId):
    context = {}
    if (request.user.pk == userId):
        utakmicesve = ""
        utakmice = Utakmiceunajavi.objects.all()
        for u in utakmice:
            u = Utakmica.objects.get(pk=u.iduta.iduta)
            utakmicesve = utakmicesve + "Timovi:\t" + u.tim1 + " - " + u.tim2 + "\t\t\tDatum i vreme:\t" + u.datumpocetka+""+"\n"

        context = {
            'utakmice': utakmicesve
        }
        return render(request, 'kvoter/aktivneutakmice.html', context)
    return render(request, 'registracija/greska.html', context)

"""
Mihailo Milenković 0117/19
Ispisivanje statistike za kvotera.
"""
@login_required(login_url='index')
def statistika(request, userId):
    context = {}
    if (request.user.pk == userId):
        stat = Statistika.objects.filter(idkor = userId)
        if not stat:
            raise Http404("Ne postoji kvoter sa unetim ID")
        stat_list = list(stat)
        podaci = stat_list[0]
        s=(podaci.brojprimljenihpogodjenih + podaci.brojprimljenihpromasenih)
        if(s==0):
            s=1
        procenat_win = round((podaci.brojprimljenihpogodjenih / s) * 100, 2)
        procenat_lose = round((podaci.brojprimljenihpromasenih / s) * 100, 2)
        context = {'podaci': podaci, 'procenat_win': procenat_win, 'procenat_lose': procenat_lose}
        return render(request, 'kvoter/statistika.html', context)
    return render(request, 'registracija/greska.html', context)

"""Anja Kovačević 0484/19
Prikaz svih tiketa koji u trenutno aktivni
"""
@login_required(login_url='index')
def prikazisvetikete(request, userId):
    context = {}
    if (request.user.pk == userId):

        tiketi=Tiket.objects.all()
        tiketi=list(tiketi)
        tiketdogadjaji=Tiketdogadjaj.objects.all()
        utakmice=Utakmica.objects.all()
        unajavi= Utakmiceunajavi.objects.all()
        nizindeksitiketa=[]
        nadjeno=0
        for t in tiketi:
            i=-1
            """Ukoliko nisu počele utakmice, tiket se dodaje u listu tiketa"""
            for td in tiketdogadjaji:
                nadjeno=0
                for u in unajavi:
                    if(td.iduta.pk == u.iduta.pk):
                        nadjeno=1
                if(nadjeno==0):
                    break
            i=i+1
            if(nadjeno==0):
                nizindeksitiketa.append(i)

        for t in nizindeksitiketa:
            tiketi.pop(t)
            for i in range(0,len(nizindeksitiketa)):
                nizindeksitiketa[i]=nizindeksitiketa[i]-1


        context={'tiketi': tiketi, 'tiketdogadjaji': tiketdogadjaji, 'utakmice': utakmice }
        return render(request, 'kvoter/prikazsvihtiketa.html', context)
    return render(request, 'registracija/greska.html', context)

"""Mihailo Milenković 0117/19
Popunjava se forma na osnovu svih tiketa i postavlja se kvota (popunjava se forma)
za vip opkladu- prolaz ili pad tiketa
"""
@login_required(login_url='index')
def postavivipkvotu(request, userId):
    context = {}
    if (request.user.pk == userId):
        greska = ""
        if(request.method=='POST'):
            form=VipKvoteForm(request.POST)
            if(form.is_valid()):
                idtik = form.cleaned_data['idtik']
                pad = form.cleaned_data['pad']
                prolaz = form.cleaned_data['prolaz']
                nematiketa=0
                tiket=0
                try:
                    """Proverava se da li postji tiket sa datim ID-em"""
                    tiket = Tiket.objects.get(pk=idtik)
                except:
                    nematiketa=1
                    greska="Tiket sa zadatim ID-em ne postoji!"

                if(nematiketa==0):
                    """Ukoliko tiket postoji pravi se vip kvota i postavlja se i upisuje se u bazu"""
                    vip = Vipkvote()
                    vip.idtik = tiket
                    vip.idkor = Kvoter.objects.get(pk=userId)
                    vip.kvotaprolaz = float(prolaz)
                    vip.kvotapad = float(pad)

                    tiketdogadjaji = Tiketdogadjaj.objects.filter(idtik=tiket.idtik)
                    unajavi = Utakmiceunajavi.objects.all()
                    nadjeno = 0

                    """Ukoliko su utakmice sa tiketa počele nemoguće je da se napravi vip kvota"""
                    for td in tiketdogadjaji:
                        nadjeno = 0
                        for u in unajavi:
                            if (td.iduta.pk == u.iduta.pk):
                                nadjeno = 1
                        if (nadjeno == 0):
                            greska = "Neke utakmice sa tiketa ID: "+idtik+"  su počele!"

                            break
                    if (nadjeno == 1):
                        greska = "Uspešno dodata vip kvota!"
                        vip.save()


        form=VipKvoteForm()
        context={'form': form, 'greska': greska }
        return render(request, 'kvoter/postavivipkvotu.html', context)
    return render(request, 'registracija/greska.html', context)