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