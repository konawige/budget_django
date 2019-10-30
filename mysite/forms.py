from django import forms
from mysite import bankChoices
from .models import Entries
from .models import BdgItems
from bootstrap_modal_forms.forms import BSModalForm

class ItemForm(BSModalForm):
    class Meta:
        model = BdgItems
        fields = ['name', 'category', 'bdgType','expected_amount']


class FileForm(forms.Form):
    bankName = forms.ChoiceField(choices=bankChoices, label='Bank')
    inputFile = forms.FileField(label="Transaction file")


class EntriesForm(forms.ModelForm):
    ignoreTransaction = forms.BooleanField(required=False, label="Discard transaction")

    class Meta:
        model = Entries
        fields = '__all__'