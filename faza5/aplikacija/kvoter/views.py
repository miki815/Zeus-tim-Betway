from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return HttpResponse("Kvoter ovde")


def napravikvote(request, userId):
    poruka=""
    if(request.method == 'POST'):
        form = KvoteForm(request.POST or None, request.FILES)
        if form.is_valid():
            prviTim = form.cleaned_data['prviTim']
            drugiTim = form.cleaned_data['drugiTim']
            datum = form.cleaned_data['datum']
            try:
                utakmica = Utakmica.objects.get(tim1=prviTim, tim2=drugiTim)
            except ObjectDoesNotExist:
                utakmica=0
                poruka="Utakmica ne postoji!"
            if(utakmica):
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
                novakvota.iduta=Utakmiceunajavi.objects.get(pk=utakmica.pk)

                novakvota.idkvo=Postavljenekvote.objects.count()+1
                novakvota.save()
                poruka="Uspesno ste dodali kvote!"
    #print(form.errors)
    form=KvoteForm()
    print(form.errors)
    context={'form': form, 'poruka': poruka}
    return render(request, 'kvoter/kvoter.html', context)

def prikaziaktivneutakmice(request, userId):
    utakmicesve = ""
    utakmice = Utakmiceunajavi.objects.all()
    for u in utakmice:
        u = Utakmica.objects.get(pk=u.iduta.iduta)
        utakmicesve = utakmicesve + "Timovi:\t" + u.tim1 + " - " + u.tim2 + "\t\t\tDatum i vreme:\t" + u.datumpocetka+""+"\n"

    context = {
        'utakmice': utakmicesve
    }
    return render(request, 'kvoter/aktivneutakmice.html', context)

def statistika(request, userId):
    stat = Statistika.objects.filter(idkor = userId)
    if not stat:
        raise Http404("Ne postoji kvoter sa unetim ID")
    stat_list = list(stat)
    podaci = stat_list[0]
    procenat_win = round((podaci.brojprimljenihpogodjenih / (podaci.brojprimljenihpogodjenih + podaci.brojprimljenihpromasenih)) * 100, 2)
    procenat_lose = round((podaci.brojprimljenihpromasenih / (podaci.brojprimljenihpogodjenih + podaci.brojprimljenihpromasenih)) * 100, 2)
    context = {'podaci': podaci, 'procenat_win': procenat_win, 'procenat_lose': procenat_lose}
    return render(request, 'kvoter/statistika.html', context)