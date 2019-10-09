from django.shortcuts import render
from mysite.models import Entries

# Create your views here.
def home(request):
    return render(request, 'mysite/base.html')

def index(request):
    """ Afficher tous les entrees dans la table """
    entries = Entries.objects.all() # Nous sélectionnons tous nos artentrees
    return render(request, 'mysite/index.html', {'all_entries': entries})