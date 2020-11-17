from django import forms
from mysite import bankChoices
from .models import Entries
from .models import BdgItems, AccountTypes
from bootstrap_modal_forms.forms import BSModalForm


class ItemForm(BSModalForm):
    class Meta:
        model = BdgItems
        fields = ['name', 'category', 'bdgType','expected_amount']


class FileForm(forms.Form):
    listBank = [(k, v) for k, v in bankChoices.items()] 
    bankName = forms.ChoiceField(choices=listBank, label='Bank')
    inputFile = forms.FileField(label="Transaction file")


class EntriesForm(forms.Form):
    date = forms.DateField()
    accountType = forms.ModelChoiceField(queryset=AccountTypes.objects.all(), label="Account type")
    item = forms.ModelChoiceField (queryset=BdgItems.objects.all(), required=False)   
    amount = forms.FloatField()
    description = forms.CharField()
    ignoreTransaction = forms.BooleanField(required=False, label="Discard transaction")


    def clean(self):
        cleaned_data = super(EntriesForm, self).clean()
        ign = cleaned_data.get('ignoreTransaction')
        item = cleaned_data.get('item')

        if (ign == False and item is None):  # if ignore is not checked and no tem is chosen, raise an error
            raise forms.ValidationError(
                    "Either discard transaction or choose item"
            )

        return cleaned_data  # return clean_data

# class DisplayForm(forms.Form):
#     month = forms.ChoiceField()
#     year = forms.ChoiceField(queryset=AccountTypes.objects.all(), label="Account type")
#     cat = forms.ModelChoiceField (queryset=BdgItems.objects.all(), required=False)

