

import os
from os.path import abspath

import pandas as pd
from django.conf import settings
from django.shortcuts import render

from mysite import listRBCCol, inputFileName, cleanedCol, RET_GOOD
from mysite.forms import FileForm, EntriesForm
from mysite.models import Entries


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

            # parse uploaded file to get list of transactions
            ret, data = parse_file(chBank,inputFileName)
            if ret == RET_GOOD:
                listData = []
                i=0
                nbRows = len(data.index)
                while i<nbRows:
                    form = EntriesForm()
                    form.fields['amount'].initial = data.iloc[i]['Amount']
                    form.fields['description'].initial = data.iloc[i]['Description']
                    form.fields['date'].initial = data.iloc[i]['Date']
                    listData.append(form)
                    i = i+1

                tabHead = ['Date','Account', 'Item','Amount','Description','Ignore']
                

                return render(request, 'mysite/confirm_entry.html', {'tabHead':tabHead,
                'listData':listData})


    
        


        bEnd = True

    return render(request, 'mysite/add_entry_file.html', {
        'form': form,
        'bEnd': bEnd,
        'f': f
    })

def ConfirmEntries(request):
    form = EntriesForm(request.POST or None)

    if form.is_valid():
        pass

    return render(request, 'mysite/confirm_entry.html', {
        'form': form,
    })


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
    rows, nbCol = data.shape


    if fBank == '1':
        if nbCol != len(listRBCCol):
            return 101, pd.DataFrame()

        if 'Type de compte' in list(data.columns):
            #data['Type de compte'] = data['Type de compte'].astype(str).replace(pat='Chèques',repl='Debit',regex=False)
            data['Type de compte'] = data['Type de compte'].astype(str).replace(to_replace='Chèques',value='Debit')
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



    
