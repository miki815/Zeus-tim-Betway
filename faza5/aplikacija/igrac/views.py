from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import DesetForm, IsplataForm

def index(request):
    return HttpResponse("Igrac ovde")

def profil(request, userId):
    status="NV"
    stanje = 1000
    form = IsplataForm()
    context = {'stanje': stanje, 'form': form, 'status': status}
    return render(request, 'igrac/profil.html', context)

def deset_u_nizu(request):
    if(request.method == 'POST'):
        form = DesetForm(request.POST)
        if(form.is_valid()):
            return HttpResponse(form.cleaned_data['ishod'])
            #TODO ubaciti izbor u bazu, redirect na statistiku igre
    else:
        form = DesetForm()
    context = {'form': form}
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