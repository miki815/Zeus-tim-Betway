from django import forms


class DodavanjeUtakmiceForm(forms.Form):
    tim1 = forms.CharField(label="Prvi tim")
    tim2 = forms.CharField(label="Drugi tim")
    datumvreme = forms.DateTimeField(label="Datum i vreme")

class DodavanjeUtakmice10Form(forms.Form):
    tim1 = forms.CharField(label="Prvi tim")
    tim2 = forms.CharField(label="Drugi tim")

class UgasiUtakmicuForm(forms.Form):
    tim1 = forms.CharField(label="Prvi tim")
    tim2 = forms.CharField(label="Drugi tim")
    datum = forms.CharField(label="Datum [01-01-2022]")
    ishod = forms.CharField(label="Ishod")

class StartujUtakmicuForm(forms.Form):
    tim1 = forms.CharField(label="Prvi tim")
    tim2 = forms.CharField(label="Drugi tim")
    datum = forms.CharField(label="Datum [01-01-2022]")
