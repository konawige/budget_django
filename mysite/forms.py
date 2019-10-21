from django import forms
from mysite import bankChoices
from .models import Entries

class FileForm(forms.Form):
    bankName = forms.ChoiceField(choices=bankChoices, label='Bank')
    inputFile = forms.FileField(label="Transaction file")


class EntriesForm(forms.ModelForm):
    class Meta:
        model = Entries
        fields = '__all__'