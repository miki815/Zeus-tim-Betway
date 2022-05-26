from django import forms


class BrisanjeNalogaForm(forms.Form):
    lozinka = forms.CharField(label="Uneti lozinku")

class KvoteForm(forms.Form):
    prviTim=forms.CharField(label="Prvi tim")
    drugiTim = forms.CharField(label="Drugi tim")
    datum = forms.DateTimeField(label="Datum")

    kec = forms.CharField(label="1")
    x = forms.CharField(label="x")
    dvojka = forms.CharField(label="2")

    jj = forms.CharField(label="1-1")
    jx = forms.CharField(label="1-x")
    jd = forms.CharField(label="1-2")

    xj = forms.CharField(label="x-1")
    xx = forms.CharField(label="x-x")
    xd = forms.CharField(label="x-2")

    dj = forms.CharField(label="2-1")
    dx = forms.CharField(label="2-x")
    dd = forms.CharField(label="2-2")

    prvigol = forms.CharField(label="Prvi gol 1")
    xgol = forms.CharField(label="Prvi gol x")
    drugigol = forms.CharField(label="Prvi gol 2")






