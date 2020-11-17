bankChoices = {1:'RBC',2:'NBC', 3:'NBC-Credit', 4:'DESJARDINS', 5:'TANGERINE',}
inputFileName = 'inputData.csv'
listRBCCol = ['Type de compte', 'Numéro du compte', "Date de l'opération", "Numéro du chèque",
              "Description 1", "Description 2", "CAD", "USD"]

listNBCCol = ['Date', 'Description', "Categorie", "Debit",
              "Credit", "Solde"]

listNBCColCredit = ['Date', 'Numero de Carte', "Description", "Categorie", "Debit",
              "Credit"]

listDesjardinsCol = ['Caisse', 'Numero', "Type", "Date", "order", 'Description', 'Empty1', 'Debit', 'Credit',
'Empty2', 'Empty3', 'Empty4', 'Empty5',"Solde"]

listTangerineCol = ["Date", "Transaction", "Nom", "Description", "Montant"]



cleanedCol = ['Date', 'Account','Amount','Description']

RET_GOOD = 100
