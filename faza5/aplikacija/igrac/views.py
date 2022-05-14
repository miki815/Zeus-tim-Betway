from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import DesetForm

def index(request):
    return HttpResponse("Igrac ovde")

def profil(request, userId):
    context = {}
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
