

import os
from fnmatch import filter
from os.path import abspath
import datetime as dt

import pandas as pd
from bootstrap_modal_forms.generic import BSModalCreateView
from django.conf import settings
from django.forms.widgets import NumberInput
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from mysite import RET_GOOD, cleanedCol, inputFileName, listRBCCol
from mysite.forms import EntriesForm, FileForm
from mysite.models import BdgItems, Entries, AccountTypes

from .forms import ItemForm
from django.forms import formset_factory


class ItemCreateView(BSModalCreateView):
    template_name = 'mysite/create_item.html'
    form_class = ItemForm
    success_message = 'Success: Item was created.'
    success_url = reverse_lazy('confirm',args=[1])


# Create your views here.
def home(request):
    return render(request, 'mysite/base.html')

def index(request):
    """ Afficher tous les entrees dans la table """
    entries = Entries.objects.all() # Nous sélectionnons tous nos entrees
    return render(request, 'mysite/index.html', {'all_entries': entries})

def addEntries(request):
    """ Add new entries """
    bEnd = False
    f = ''
    form = FileForm(request.POST or None, request.FILES)

    if form.is_valid():
        #Get the bank choice
        chBank = form.cleaned_data['bankName']
        f = request.FILES['inputFile']

        if f.name.endswith('.csv'):
            save_uploaded_file(f)
            return HttpResponseRedirect(reverse('confirm', args=[chBank]))

        bEnd = True

    return render(request, 'mysite/add_entry_file.html', {
        'form': form,
        'bEnd': bEnd,
        'f': f
    })

def ConfirmEntries(request,intBank):

    # parse uploaded file to get list of transactions
    ret, data = parse_file(intBank,inputFileName)
    if ret == RET_GOOD:
        nbRows = len(data.index)
        EntriesFormSet = formset_factory(EntriesForm, extra=nbRows-1)
        formset = EntriesFormSet(request.POST or None)
        i=0
        for form in formset:
            form.fields['item'].required = False
            form.fields['amount'].initial = abs(data.iloc[i]['Amount'])                    
            form.fields['description'].initial = data.iloc[i]['Description']
            form.fields['accountType'].initial = AccountTypes.objects.get(name=data.iloc[i]['Account'])
            entryDate = dt.datetime.strptime(str(data.iloc[i]['Date']),"%m/%d/%Y")             
            form.fields['date'].initial = "{}-{}-{}".format(entryDate.year, entryDate.month, entryDate.day)

            # check for duplicate
            #form.fields['date'].initial,
            if Entries.objects.filter(date= entryDate, amount__range=(form.fields['amount'].initial-0.5, form.fields['amount'].initial+0.5)):
                form.fields['ignoreTransaction'].initial = True
            
            i = i+1

        if formset.is_valid():
            for elt in formset.cleaned_data:
                if elt['ignoreTransaction'] == False:
                    insert = Entries(date=elt['date'], amount=elt['amount'],description=elt['description'],
                                     accountType=elt['accountType'], item=elt['item'])
                    insert.save() 

            return HttpResponseRedirect(reverse('view_all'))
        

        return render(request, 'mysite/confirm_entry.html', {'formset':formset, 'intBank':intBank})



def save_uploaded_file(f):
    folder = os.path.join(settings.MEDIA_ROOT,'data')

    if not os.path.exists(folder):
         os.makedirs(folder)
    elif not os.path.isdir(folder):
         return #you may want to throw some error or so.
    with open(os.path.join(folder, inputFileName), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def parse_file(fBank, fName):
    folder = os.path.join(settings.MEDIA_ROOT,'data')

    data = pd.read_csv(os.path.join(folder, fName),encoding='latin-1',index_col=False)
    nbCol = data.shape[1]


    if fBank == 1:
        if nbCol != len(listRBCCol):
            return 101, pd.DataFrame()

        if 'Type de compte' in list(data.columns):
            #data['Type de compte'] = data['Type de compte'].astype(str).replace(pat='Chèques',repl='Debit',regex=False)
            data['Type de compte'] = data['Type de compte'].astype(str).replace(to_replace='Chèques',value='debit')
            data = data.rename(columns={'Type de compte':'Account'})
        else:
            return 102, pd.DataFrame()

        if "Date de l'opération" in list(data.columns):
            data = data.rename(columns={"Date de l'opération":'Date'})
        else:
            return 102, pd.DataFrame()

        if 'Description 1' in list(data.columns) and 'Description 2' in list(data.columns):
            data['Description'] = data['Description 1'].astype(str) + ' / '+ data['Description 2'].astype(str)
        else:
            return 102, pd.DataFrame()

        if 'CAD' in list(data.columns):
            data = data.rename(columns={"CAD":'Amount'})
        else:
            return 102, pd.DataFrame()

        data = data[cleanedCol]

        return 100, data
