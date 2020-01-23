bankChoices = {1:'RBC',2:'NBC', 3:'DESJARDINS', 4:'TANGERINE', 5:'NBC-Credit'}
inputFileName = 'inputData.csv'
listRBCCol = ['Type de compte', 'Numéro du compte', "Date de l'opération", "Numéro du chèque",
              "Description 1", "Description 2", "CAD", "USD"]

listNBCCol = ['Date', 'Description', "Categorie", "Debit",
              "Credit", "Solde"]

cleanedCol = ['Date', 'Account','Amount','Description']

RET_GOOD = 100
