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
                if tip.brojpogodaka == 10: # pobednik, kraj igre
                  #  korisnik = Korisnik.objects.filter(idkor = tip.idkor)
                    korisnik = tip.idkor
                    korisnik.vip = 1
                    if not korisnik.stanje:
                        korisnik.stanje = 0
                    korisnik.stanje += 1000
                    korisnik.save()
                    for tips in tipovi:
                        tips.brojpogodaka = 0 # reset all
                        tips.validno = False
                        tips.save()
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
