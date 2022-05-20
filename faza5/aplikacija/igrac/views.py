from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import *
from .models import *
from datetime import date


def index(request):
    return HttpResponse("Igrac ovde")

def profil(request, userId):
    status="NV"
    stanje = 1000
    form = IsplataForm()
    context = {'stanje': stanje, 'form': form, 'status': status, 'userId': userId}
    return render(request, 'igrac/profil.html', context)

def deset_u_nizu(request, userId):
    if(request.method == 'POST'):
        form = DesetForm(request.POST)
        if(form.is_valid()):
            ishod = form.cleaned_data['ishod']
            igra = Desetunizu.objects.filter(idkor = userId)
            if not igra:
                # todo ubaci u bazu
                pass
            igra_list = list(igra)
            moja_igra = igra_list[0]
            moja_igra.validno = True
            moja_igra.odigrano = ishod
            moja_igra.save()
            return HttpResponse(form.cleaned_data['ishod'])
            #TODO ubaciti izbor u bazu, redirect na statistiku igre
    else:
        form = DesetForm()
    indeks = Utakmica10.objects.count()
    utakmica = Utakmica10.objects.all()
    utakmica = utakmica[indeks - 1]
    utakmica = utakmica.utakmica10
    context = {'form': form, 'userId': userId,  'utakmica': utakmica}
    return render(request, 'igrac/desetunizu.html', context)




def isplati(request):
    stanje=1000
    iznos=0
    if (request.method == 'POST'):
        form = IsplataForm(request.POST)
        if (form.is_valid()):
            iznos = form.cleaned_data['iznos']
            if(stanje>=iznos):
                stanje=stanje-iznos
            context = {'form': form, 'stanje': stanje}
            return render(request, 'igrac/profil.html', context)
            # TODO ubaciti izbor u bazu, redirect na statistiku igre
    else:
        form = IsplataForm()
    context = {'form': form, 'stanje': stanje}
    return render(request, 'igrac/profil.html', context)

def promenalozinke(request, userId):
    poruka=""
    if (request.method == 'POST'):
        form = PromenaLozinkeForm(request.POST)
        if (form.is_valid()):
            korisnik = Korisnik.objects.get(pk=userId)
            lozinka0 = form.cleaned_data['lozinka0']
            lozinka1=form.cleaned_data['lozinka1']
            lozinka2 = form.cleaned_data['lozinka2']
            if(lozinka0!=korisnik.lozinka):
                poruka = "Netacna lozinka!"
                context = {'form': form, 'poruka': poruka}

                return render(request, 'igrac/promenalozinke.html', context)
            if (lozinka2 != lozinka1):
                poruka="Lozinka za potvrdu nije ista!"
                context = {'form': form, 'poruka': poruka}
                return render(request, 'igrac/promenalozinke.html', context)
            else:
                poruka = "Uspesno ste promenili lozinku!"
                korisnik.lozinka = lozinka1
                korisnik.save()
                context = {'form': form, 'poruka': poruka}
                return render(request, 'igrac/promenalozinke.html', context)
    else:
        form=PromenaLozinkeForm()
        context={'form': form, 'poruka': poruka}
    return render(request, 'igrac/promenalozinke.html', context)


def brisanjenaloga(request, userId):
    poruka=""
    context={}
    if (request.method == 'POST'):
        form = BrisanjeNalogaForm(request.POST)
        if (form.is_valid()):
            korisnik = Korisnik.objects.get(pk=userId)
            lozinka = form.cleaned_data['lozinka']
            if(korisnik.lozinka==lozinka):

                return render(request, 'igrac/brisanjeporuka.html', context)
            else:
                poruka="Netacna lozinka!"
        context = {'form': form, 'poruka': poruka}
        return render(request, 'igrac/brisanjenaloga.html', context)
    else:
        form=BrisanjeNalogaForm()
        context={'form': form, 'poruka': poruka}
    return render(request, 'igrac/brisanjenaloga.html', context)

def registracija(request):
    context = {}
    return render(request, 'igrac/rregistracija.html', context)


def brisanjeporuka(request,userId ):

    form = BrisanjeNalogaForm(request.POST)
    context = {'form': form}
    aa=request.POST.get('DA')
    if (request.method == 'POST'):
      if (request.POST.get('DA')):
          Korisnik.objects.filter(pk=userId).delete()
          return render(request, 'igrac/rregistracija.html', context)
      else:
          return render(request, 'igrac/brisanjenaloga.html', context)

    return render(request, 'igrac/brisanjeporuka.html', context)


def postanivip(request, userId):
    korisnik = Korisnik.objects.get(pk=userId)
    stanje = korisnik.stanje
    v=korisnik.vip
    if (request.method == 'POST'):
        if(korisnik.vip == 0):
            form = VipForm(request.POST)
            if (form.is_valid()):
                x = form.cleaned_data['vip']
                if (x == '1'):
                    if (stanje >= 1000):
                        stanje = stanje - 1000

                if (x == '2'):
                    if (stanje >= 5000):
                        stanje = stanje - 5000
                if (x == '3'):
                    if (stanje >= 9000):
                        stanje = stanje - 9000
                korisnik.vip = 1
                korisnik.stanje=stanje
                korisnik.save()

    form=VipForm()
    context={'form': form, 'stanje': stanje}
    return render(request, 'igrac/postanivip.html', context)

def prikaz_kvotera(request, userId):
    kvoteri = Korisnik.objects.all() #TODO iz tabele kvoter a ne korisnik

    context = {'kvoteri': kvoteri, 'userId': userId}
    return render(request, 'igrac/prikazKvotera.html', context)


def prikaz_kvota(request, kvoterId, igracId):
    kvote = Postavljenekvote.objects.filter(idkor = kvoterId)
    utakmice = []
    for kvota in kvote:
         utakmice.append(kvota.iduta)

    if request.method == 'POST':
        ukupna_kvota = 1;
        uplata = request.POST.get("fname")
        tiket = Tiket()
        tiket.save()
        for kvota in kvote:
            data_id = "test" + kvota.idkvo
            data = request.POST.get(data_id)
            if data:
                ukupna_kvota *= float(data);
                par_na_tiketu = Tiketdogadjaj()
                par_na_tiketu.odigrano = False
                par_na_tiketu.iduta = kvota.iduta
                par_na_tiketu.kvota = data
                par_na_tiketu.idtik = tiket
                par_na_tiketu.save()
        tiket.kvota = ukupna_kvota
        tiket.iznosuplate = uplata
        tiket.dobitak = ukupna_kvota * int(uplata)
        kvoter = list(Kvoter.objects.filter(idkor=kvoterId))
        tiket.idkvo = kvoter[0]
        igrac = list(Igrac.objects.filter(idkor=igracId))
        tiket.idkor = igrac[0]
        tiket.datumuplate = date.today()
        tiket.save()
        return HttpResponse("Vas tiket je uplacen")

    kvote_utakmice = zip(kvote, utakmice)
    context={'kvote_utakmice': kvote_utakmice, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId}
    return render(request, 'igrac/kvote.html', context)


def uplati_tiket(request):
    return HttpResponse("todo")

def statistika(request, userId):
    stat = Statistika.objects.filter(idkor = userId)
    if not stat:
        raise Http404("Ne postoji igrac sa unetim ID")
    stat_list = list(stat)
    podaci = stat_list[0]
    procenat_win = round((podaci.brojpogodjenih / (podaci.brojpogodjenih + podaci.brojpromasenih)) * 100, 2)
    procenat_lose = round((podaci.brojpromasenih / (podaci.brojpogodjenih + podaci.brojpromasenih)) * 100, 2)
    context = {'podaci': podaci, 'procenat_win': procenat_win, 'procenat_lose': procenat_lose}
    return render(request, 'igrac/statistika.html', context)

def najbolji(request):
    korisnici=Korisnik.objects.all()
    s=Statistika.objects.all()
    najbolji=Statistika.objects.order_by('-ukupnodobijeno')
    brojprimljenih = Statistika.objects.order_by('-brojprimljenihpogodjenih')
    context={'igraci': korisnici, 'statistike': najbolji, 'brojprimljenih': brojprimljenih}
    return   render(request, 'igrac/najbolji.html', context)


