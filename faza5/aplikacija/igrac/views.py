from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import *
from .models import *
from datetime import date


def index(request):
    return HttpResponse("Igrac ovde")

def profil(request, userId):
    igrac = Korisnik.objects.filter(idkor = userId)
    igrac = list(igrac)
    igrac = igrac[0]
    status= "VIP" if igrac.vip else "REGULAR"
    stanje = igrac.stanje if igrac.stanje else 0
    statistika = Statistika.objects.filter(idkor = userId)
    statistika = list(statistika)
    statistika = statistika[0]
    brojPogodaka = statistika.brojpogodjenih
    brojPromasaja = statistika.brojpromasenih
    widthPogodaka = (brojPogodaka / (brojPogodaka + brojPromasaja)) * 100
    widthPromasaja = (brojPromasaja / (brojPogodaka + brojPromasaja)) * 100
    korisnickoIme = igrac.korisnickoime
    iznos=0

    if (request.method == 'POST'):
        form = IsplataForm(request.POST)
        if (form.is_valid()):
            iznos = form.cleaned_data['iznos']
            if(stanje>=iznos):
                stanje=stanje-iznos
                igrac.stanje = stanje
                igrac.save()

    form = IsplataForm()
    context = {'stanje': stanje, 'form': form, 'status': status, 'userId': userId, 'brojPogodaka': brojPogodaka,
               'brojPromasaja': brojPromasaja, 'korisnickoIme': korisnickoIme, 'wProm': widthPromasaja,
               'wPog': widthPogodaka}
    return render(request, 'igrac/profil.html', context)

def deset_u_nizu(request, userId):
    igra = Desetunizu.objects.filter(idkor=userId)
    igra_list = list(igra)
    moja_igra = igra_list[0]
    brojPogodaka = moja_igra.brojpogodaka
    if(request.method == 'POST'):
        form = DesetForm(request.POST)
        if(form.is_valid()):
            ishod = form.cleaned_data['ishod']
            moja_igra.validno = True
            moja_igra.odigrano = ishod
            moja_igra.save()
            igraci = list(Desetunizu.objects.all())
            for i in range(len(igraci) - 1):
                for j in range(0, len(igraci) - 1 - i):
                    if(igraci[j].brojpogodaka < igraci[j+1].brojpogodaka):
                        igraci[j], igraci[j+1] = igraci[j+1], igraci[j]
            context = {'userId': userId, 'igraci': igraci}
            return render(request, 'igrac/desetunizuinfo.html', context)
    else:
        form = DesetForm()
    indeks = Utakmica10.objects.count()
    utakmica = Utakmica10.objects.all()
    utakmica = utakmica[indeks - 1]
    utakmica = utakmica.utakmica10
    context = {'form': form, 'userId': userId,  'utakmica': utakmica, 'brojPogodaka': brojPogodaka}
    return render(request, 'igrac/desetunizu.html', context)


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
    poruka=""
    korisnik = Korisnik.objects.get(pk=userId)
    stanje = korisnik.stanje
    v=korisnik.vip
    if (request.method == 'POST'):
        if(korisnik.vip == 0):
            form = VipForm(request.POST)
            if (form.is_valid()):
                x = form.cleaned_data['vip']
                v=0
                if (x == '1'):
                    if (stanje >= 1000):
                        stanje = stanje - 1000
                        v=30

                if (x == '2'):
                    if (stanje >= 5000):
                        stanje = stanje - 5000
                        v=183
                if (x == '3'):
                    if (stanje >= 9000):
                        stanje = stanje - 9000
                        v=365
                if(v):
                    korisnik.vip = v
                    korisnik.stanje=stanje
                    korisnik.save()
                    poruka="Uspesno ste postali VIP korisnik!"
                else:
                    poruka="Nemate dovoljno novca da postanete vip"
    form=VipForm()
    context={'form': form, 'stanje': stanje, 'poruka': poruka, 'userId': userId}
    return render(request, 'igrac/postanivip.html', context)

def prikaz_kvotera(request, userId):
    kvoteri = Korisnik.objects.all() #TODO iz tabele kvoter a ne korisnik

    context = {'kvoteri': kvoteri, 'userId': userId}
    return render(request, 'igrac/prikazKvotera.html', context)


def prikaz_kvota(request, kvoterId, igracId):
    kvote = Postavljenekvote.objects.filter(idkor = kvoterId)
    utakmice = []
    poruka = 0;
    for kvota in kvote:
         utakmice.append(kvota.iduta)
    kvote_utakmice = zip(kvote, utakmice)

    if request.method == 'POST':
        igrac = list(Igrac.objects.filter(idkor=igracId))
        kvoter = list(Kvoter.objects.filter(idkor=kvoterId))
        korisnik = list(Korisnik.objects.filter(idkor=igracId))
        korisnikKvoter = list(Korisnik.objects.filter(idkor=kvoterId))
        ukupna_kvota = 1;
        uplata = request.POST.get("fname")
        if korisnik[0].stanje < int(uplata):
            poruka = "Nemate dovoljno novca da uplatite tiket!"
            return render(request, 'igrac/kvote.html', {'poruka': poruka,'kvote_utakmice': kvote_utakmice, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId})
        if int(uplata) < 20:
            poruka = "Minimalna uplata iznosi 20!"
            return render(request, 'igrac/kvote.html', {'poruka': poruka, 'kvote_utakmice': kvote_utakmice, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId})
        tiket = Tiket()
        tiket.save()
        for kvota in kvote:
            data_id = "test" + kvota.idkvo
            odigrano_id = "odigrano" + kvota.idkvo
            data = request.POST.get(data_id)
            odigrano = request.POST.get(odigrano_id)
            if data != "nula":
                ukupna_kvota *= float(data);
                par_na_tiketu = Tiketdogadjaj()
                par_na_tiketu.odigrano = odigrano
                par_na_tiketu.iduta = kvota.iduta
                par_na_tiketu.kvota = data
                par_na_tiketu.idtik = tiket
                par_na_tiketu.ishod = -1
                par_na_tiketu.save()
        if(ukupna_kvota == 1):
            tiket.delete();
            poruka = "Niste izabrali tipove!"
            return render(request, 'igrac/kvote.html', {'poruka': poruka, 'kvote_utakmice': kvote_utakmice,
                                                        'kvoterId': kvoterId, 'kvote': kvote,'igracId': igracId})
        if ukupna_kvota * int(uplata) + int(uplata) >  korisnikKvoter[0].stanje:
            poruka = "Kvoter nema novca da vam isplati dobitak! Max uplata za ovaj tiket: " + str(float(korisnikKvoter[0].stanje) / ukupna_kvota)
            context = {'kvote_utakmice': kvote_utakmice, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId,
                   'poruka': poruka}
            return render(request, 'igrac/kvote.html', context)
        korisnik[0].stanje -= int(uplata)
        korisnik[0].save()
        korisnikKvoter[0].stanje += int(uplata)
        korisnikKvoter[0].save()
        tiket.kvota = ukupna_kvota
        tiket.iznosuplate = uplata
        tiket.dobitak = ukupna_kvota * int(uplata)
        tiket.idkvo = kvoter[0]
        tiket.idkor = igrac[0]
        tiket.datumuplate = date.today()
        tiket.save()
        poruka="Uspešno ste uplatili tiket!"


    context={'kvote_utakmice': kvote_utakmice, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId, 'poruka': poruka}
    return render(request, 'igrac/kvote.html', context)


def uplati_tiket(request,userId):
    return HttpResponse("todo")

def statistika(request, userId):
    stat = Statistika.objects.filter(idkor = userId)
    if not stat:
        raise Http404("Ne postoji igrac sa unetim ID")
    stat_list = list(stat)
    podaci = stat_list[0]
    procenat_win = round((podaci.brojpogodjenih / (podaci.brojpogodjenih + podaci.brojpromasenih)) * 100, 2)
    procenat_lose = round((podaci.brojpromasenih / (podaci.brojpogodjenih + podaci.brojpromasenih)) * 100, 2)
    context = {'userId': userId, 'podaci': podaci, 'procenat_win': procenat_win, 'procenat_lose': procenat_lose}
    return render(request, 'igrac/statistika.html', context)

def najbolji(request, userId):
    korisnici=Korisnik.objects.all()
    s=Statistika.objects.all()
    najbolji=Statistika.objects.order_by('-ukupnodobijeno')
    brojprimljenih = Statistika.objects.order_by('-brojprimljenihpogodjenih')
    context={'igraci': korisnici, 'statistike': najbolji, 'brojprimljenih': brojprimljenih, 'userId': userId}
    return   render(request, 'igrac/najbolji.html', context)

def prikaz_vip_kvotera(request, userId):
    kvoteri = Korisnik.objects.all()
    vip_kvoteri = []
    for kvoter in kvoteri:
        if kvoter.vip:
            vip_kvoteri.append(kvoter)
    context = {'kvoteri': vip_kvoteri, 'userId': userId}
    return render(request, 'igrac/prikazVipKvotera.html', context)


def prikaz_vip_kvota(request, kvoterId, igracId):
    kvote = Vipkvote.objects.filter(idkor = kvoterId)
    tiketi = []
    igraci_tiketa = []
    tiketi_podaci = [] # lista koja sadrzi liste odigranih tiketa
    poruka = 0
    for kvota in kvote:
         tiketi.append(kvota.idtik)
    kvote_tiketi = zip(kvote, tiketi)

    for tiket in tiketi:
        tiket_dogadjaji = Tiketdogadjaj.objects.filter(idtik = tiket.idtik)
        tiket_dogadjaji = list(tiket_dogadjaji)
        utakmice = []
        for dogadjaj in tiket_dogadjaji:
            utakmica = dogadjaj.iduta
            utakmica_podaci = []
            utakmica_podaci.append(utakmica.tim1)
            utakmica_podaci.append(utakmica.tim2)
            utakmica_podaci.append(dogadjaj.odigrano)
            utakmice.append(utakmica_podaci)
        tiketi_podaci.append(utakmice)
        igraci_tiketa.append(tiket.idkor)
    kvote_igraci_tiketi = zip(kvote, igraci_tiketa, tiketi_podaci)

    if request.method == 'POST':
        ukupna_kvota = 1;
        uplata = request.POST.get("fname")
        kvoter = list(Kvoter.objects.filter(idkor=kvoterId))
        igrac = list(Igrac.objects.filter(idkor=igracId))
        korisnik = list(Korisnik.objects.filter(idkor=igracId))
        korisnikKvoter = list(Korisnik.objects.filter(idkor=kvoterId))

        if korisnik[0].stanje < int(uplata):
            poruka = "Nemate dovoljno novca da uplatite tiket!"
            return render(request, 'igrac/vipkvote.html',
                          {'kvote_tiketi': kvote_tiketi, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId,
                           'kvote': kvote, 'kvote_igraci_tiketi': kvote_igraci_tiketi, 'tiketi': tiketi_podaci, 'poruka': poruka})
        if int(uplata) < 20:
            poruka = "Minimalna uplata iznosi 20!"
            return render(request, 'igrac/vipkvote.html',
                          {'kvote_tiketi': kvote_tiketi, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId,
                           'kvote': kvote, 'kvote_igraci_tiketi': kvote_igraci_tiketi, 'tiketi': tiketi_podaci, 'poruka': poruka})

        vip_tiket = Viptiket()
        vip_tiket.save()
        data = request.POST.get("kvota")
        odigrano = request.POST.get("odigrano")
        idKvote = request.POST.get("idKvote")
        if data:
            ukupna_kvota = float(data);
        if ukupna_kvota * int(uplata) + int(uplata) > korisnikKvoter[0].stanje:
            poruka = "Kvoter nema novca da vam isplati dobitak! Max uplata za ovaj tiket: " + str(float(korisnikKvoter[0].stanje) / ukupna_kvota)
            return render(request, 'igrac/vipkvote.html',
                          {'kvote_tiketi': kvote_tiketi, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId,
                           'kvote': kvote, 'kvote_igraci_tiketi': kvote_igraci_tiketi, 'tiketi': tiketi_podaci, 'poruka': poruka})

        vip_tiket.kvota = ukupna_kvota
        vip_tiket.iznosuplate = uplata
        vip_tiket.dobitak = ukupna_kvota * int(uplata)
        vip_tiket.idkvo = kvoter[0]
        vip_tiket.idkor = igrac[0]
        vip_tiket.datumuplate = date.today()
        vip_tiket.odigrano = odigrano
        moja_kvota = list(Vipkvote.objects.filter(idkvo = idKvote))
        moja_kvota = moja_kvota[0]
        vip_tiket.idtik = moja_kvota.idtik
        korisnik[0].stanje -= int(uplata)
        korisnik[0].save()
        korisnikKvoter[0].stanje += int(uplata)
        korisnikKvoter[0].save()
        vip_tiket.save()
        poruka = "Uspešno ste uplatili tiket!"

    context={'kvote_tiketi': kvote_tiketi, 'kvoterId': kvoterId, 'kvote': kvote, 'igracId': igracId, 'kvote': kvote,
            'kvote_igraci_tiketi': kvote_igraci_tiketi, 'tiketi': tiketi_podaci, 'poruka': poruka }
    return render(request, 'igrac/vipkvote.html', context)

def istorija(request, userId):
    utakmice=Istorijautakmica.objects.filter(idkor=userId)

    context={'utakmice': utakmice, 'userId': userId}
    return  render(request, 'igrac/istorijaodigranih.html', context)




