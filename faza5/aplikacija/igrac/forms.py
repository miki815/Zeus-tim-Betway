from django import forms

ISHODI = [('kec', '1'), ('iks', 'x'), ('dvojka', '2')]

class DesetForm(forms.Form):
    ishod = forms.ChoiceField(choices=ISHODI, widget=forms.RadioSelect)