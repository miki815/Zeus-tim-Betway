from django import forms


class DodavanjeUtakmiceForm(forms.Form):
    tim1 = forms.CharField(label="Prvi tim")
    tim2 = forms.CharField(label="Drugi tim")
    datumvreme = forms.DateTimeField(label="Datum i vreme")