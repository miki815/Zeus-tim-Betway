from django import forms

ISHODI = [('1', '1'), ('x', 'x'), ('2', '2')]
VIP=[('1','Mesec dana: 1000RSD'),('2','Sest meseci: 5000RSD'),('3','Godinu dana: 9000RSD')]

class DesetForm(forms.Form):
    ishod = forms.ChoiceField(choices=ISHODI, widget=forms.RadioSelect)

class VipForm(forms.Form):
    vip = forms.ChoiceField(choices=VIP, widget=forms.RadioSelect)

class IsplataForm(forms.Form):
    iznos=forms.IntegerField(label="Uneti iznos za isplatu: ", initial=0)

class UplataForm(forms.Form):
    uplata=forms.IntegerField(label="Uneti iznos za uplatu: ", initial=0)

class PromenaLozinkeForm(forms.Form):
    lozinka0 = forms.CharField(label="Stara lozinka")
    lozinka1=forms.CharField(label="Nova lozinka")
    lozinka2 = forms.CharField(label="Uneti ponovo novu lozinku")

class BrisanjeNalogaForm(forms.Form):
    lozinka = forms.CharField(label="Uneti lozinku")