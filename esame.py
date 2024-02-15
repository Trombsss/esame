#==============================
#  Classe per file CSV
#==============================


class ExamException(Exception):
    pass


# raise ExamException('Errore, lista valori vuota')


class CSVTimeSeriesFile:

    def __init__(self, name):

        # Setto il nome del file
        self.name = name
    
    def get_data(self):

        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except ExamException as erroreApertura:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(erroreApertura))

        else:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []

            # Apro il file con with così non serve poi chiuderlo
            with open(self.name, 'r') as my_file:

                # Leggo il file linea per linea
                for line in my_file:
                    
                    # print('---')
                    # linea csv
                    # print(line)

                    # Faccio lo split di ogni linea sulla virgola
                    elements = line.split(',')

                    # ANNO
                    # print('\t',el[0])
                    # MESE
                    # print('\t',el[1])
                    # VALORE
                    # print('\t', elements[1])

                    if elements[0] != 'date':
                        
                        # el sarà la lista dove splitterò separatamente anno e mese
                        el = []
                        el = elements[0].split('-')
                        
                        # controllo che le linee del file sia norme alle condizioni
                        try:

                            # controllo se gli elementi sono  tutti int
                            int(el[0])
                            int(el[1])
                            int(elements[1])

                            # controllo che la stringa sia formata da sole cifre 
                            # numeriche, altrimenti alzo un ExamException
                            if fail_lung(elements) is not True:
                                raise ExamException('Stringa non conforme: errore di dimensione data')

                            # controllo che la riga non abbia valori negativi
                            if int(el[0]) <= 0 or int(el[1]) <= 0 or int(elements[1]) <= 0:
                                raise ExamException('Valore negativo non accettato')

                        # uso una Exception per poter bypassare il problema e non 
                        # stoppare il programma alla prima riga errata
                        except Exception as erroreRiga:
                            print('Stringa non conforme: "{}"'.format(erroreRiga))
                            pass
                        else:
                            # Posso anche pulire il carattere di newline
                            # dall'ultimo elemento con la funzione strip():
                            elements[-1] = elements[-1].strip()

                            # p.s. in realta' strip() toglie anche gli spazi
                            # bianchi all'inizio e alla fine di una stringa.

                            # isalpha controlla se la stringa contiene delle lettere
                            if elements[0].isalpha() is not True:
                                
                                
                                # Aggiungo alla lista gli elementi di questa linea
                                # elements[1] = int(elements[1])
                                data.append(elements)
                                
                
                # controllo che la il file sia ordinato
                ordinato(data)
                
                # Quando ho processato tutte le righe, ritorno i dati
                return data


# metodo per controllare che la stringa data, formata da anno e mese
# sia di sette caratteri (compreso il trattino)
def fail_lung(el):
    if len(el[0]) == 7:
        return True
    return False


# creo una funzione per controllare che il file csv sia in ordine corretto
# e che non abbia ripetizioni
def ordinato(time_series):

    
    # creo una flag per controllare che quello analizzato non sia il primo elemento
    # ovvero per creare una variabile save ove salvare la prima data
    # per poi confrontarla con il resto
    flag = False
    anno_mese = []

    for elements in time_series:

        # controllo di non star lavorando su una stringa
        if elements[0].isalpha() is False:
            
            # splitto gli elementi per avere i valori che mi interessano
            # ovvero anno e mese  

            data = str(elements[0])
            
            anno_mese = []

            # anno_mese deve essere una lista per poter accedere
            # agli indirizzi (ovvero [1] o [0])
            anno_mese = data.split('-')

            # print(anno_mese[0])
            # anno_mese[0] = anno
            # anno_mese[1] = mese

            # se la flag è falsa allora non entra nel ciclo, poichè 
            # le variabili non sono state ancora instanziate
            # non si potrebbe paragonare il vecchio con il nuovo
            if flag is True:

                # per poter fare calcoli usando queste variabili devo 
                # metterle sotto forma di int
                oldA = int(oldA)
                newA = int(anno_mese[0])
                oldM = int(oldM)
                newM = int(anno_mese[1])
    
                #print('---')
                #print('\t', oldA)
                #print('\t\t', newA)
                #print('\t\t\t', oldM)
                #print('\t\t\t\t', newM)

                # calcolo la differenza tra i vari anni per poi
                # saper le possibili situazioni
                ra = oldA - newA
                rm = oldM - newM

                # se la differenza tra gli anni è minore di 0 (1950-1951 = -1)
                # allora entro nell'if
                if ra<=0:
                    # setto il vecchio anno come l'anno corrente per poi 
                    # paragonarlo al prossimo
                    oldA = newA

                    # se la differenza tra gli anni è 0 allora so che sono
                    # ancona nello stesso anno
                    # quindi passo al controllo dei mesi
                    if ra == 0:
                        
                        # se la differenza tra i mesi è di 0, allora 
                        # significa che gli elementi si ripetono
                        # (due mesi uguali => 10-10 = 0)
                        if rm == 0:
                            raise ExamException('Elementi si ripetono nel file')

                        # se la differenza tra i mesi è > di 0, allora 
                        # significa che un mese viene prima dell'altro
                        # in modo non cronologico
                        # (10-8 = 2)
                        if rm > 0:
                            raise ExamException('Ordine cronologico sballato: MESI')

                    # salvo l'anno attuale fuori dal for
                    oldM = newM
                else:
                    raise ExamException('Ordine cronologico sballato: ANNO')
                
            else:
                # nel caso sia il primo ciclo, setto la 
                # flag a true e setto gli anni e mesi vecchi
                flag = True
                oldA = anno_mese[0]
                oldM = anno_mese[1]


    
        
        
        
# funzione per controllare che l'anno specificato esista / abbia
# dei valori al suo interno
def check(time_series, y):
    flag = False
    l = []

    # cast y per assicurarmi di poterlo paragonare a anno_mese[0] che è una string
    y = str(y)

    for row in time_series:

        # casto le righe in stringhe
        e = str(row[0])

        # splitto l'elemento[0] formato da anno-mese
        # in una lista anno_mese
        anno_mese = e.split('-')

        # se l'anno specificato e il mese corrispondono, procedo con la verifica
        if y == anno_mese[0]:

            l.append(row[1])

            if len(l) >= 1:
                flag = True

    return flag


# funzione per controllare se l'estremo è contenuto nel file
def inCSV(time_series, y):
    
    # cast y per assicurarmi di poterlo paragonare a anno_mese[0] che è una string
    y = str(y)
    anno_mese = []
    
    for elements in time_series:

        data = str(elements[0])
        
        # print(data)
        # casto le righe in stringhe
        data = str(elements[0])

        # splitto l'elemento[0] formato da anno-mese
        # in una lista anno_mese
        anno_mese = data.split('-')

        # se l'anno specificato e il mese corrispondono, procedo con la verifica
        if y == anno_mese[0]:
                return True

   
    raise ExamException

# creo una funzione che riconosca i mesi in uno specifico anno e faccia la media dei
# corrispettivi valori
def year(time_series, y):
    y = str(y)
    anno_mese = []
    mesi = []
    valori = []

    # suddivido il file in righe
    for element in time_series:

        # casto le righe in stringhe
        e = str(element[0])

        # splitto l'elemento[0] formato da anno-mese
        # in una lista anno_mese
        anno_mese = e.split('-')

        # salvo il l'anno corrente (nel ciclo del for) in una variabile per poi
        # confrontare l'anno del ciclo con l'anno richiesto nella funzione
        annoA = anno_mese[0]

        # element[1] sarebbero i valori correlati alle date (estrapolati nel primo for)
        # print(element[1])

        # vedo i mesi per lo stesso anno, se corrispondono, allora sono nell'annata
        # richiesta nella funzione
        #print(y)
        if annoA == y:
            mesi.append(anno_mese[1])

            # se esiste l'anno e il mese, ma manca il valore, inserisco come valore 0
            if element[1] is None:
                valori.append(0)
            else:
                valori.append(element[1])

    # c è la lunghezza del vettore mesi
    # => so quanti mesi ho nel preciso anno
    c = len(mesi)
    # print(c)
    media = 0

    # creo un for per fare la media di tutti i valori in quell'anno
    # sfruttando il fatto che conosco la quantità di mesi
    for i in range(0, c):
        valori[i] = int(valori[i])
        media += valori[i]

    # faccio il calcolo della media
    finale = media / c

    return finale


# funzione per confrontare due annate
def confronta(time_series, y1, y2):

    # salvo il primo valore media in m1 e salvo il secondo in m2
    m1 = year(time_series, y1)
    #print('\t', m1)
    m2 = year(time_series, y2)
    #print('\t', m2)

    # salvo la differenza
    dif = m1 - m2

    # restituisco la differenza tra i due anni
    return dif


# funzione che restituisce un dizionare con tutti gli incrementi annuali
def compute_increments(time_series, first_year, last_year):

    # casto gli anni e da string li setto a int
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except ExamException as nonInt:
        print('I valori inseriti non sono numeri"{}"'.format(nonInt))
    try:

        inCSV(time_series, first_year)
        inCSV(time_series, last_year)
    except ExamException as annoCompreso:
        print('l\'anno da lei selezionato non esiste nel file"{}"'.format(annoCompreso))
    else:
        # creo la differenza tra i due anni per vedere quanti cicli dover fare nel for
        diff = first_year - last_year
        # uso il valore assoluto per evitare problemi
        diff = abs(diff)
        l = []

        # se l'intervallo è solo di due anni e una delle due liste è vuota, allora
        # ritorno una lista vuota
        if diff <= 2 and (check(time_series, first_year) is False
                          or check(time_series, last_year) is False):
            return l

        # pongo y0 come primo anno
        y0 = first_year
        # definisco il dizionario
        dMed = {}

        y = first_year

        # creo un controllo per visualizzare solo gli anni che hanno dei valori
        # per poi salvarli in l
        for i in range(diff + 1):
            #print('----')
            #print(y)
            #print(check(time_series, y))
            #print('----')
            flag = check(time_series, y)

            if flag is True:
                l.append(y)

            y += 1

        dim = len(l)

        #print('---')
        #print(l)
        #print(dim)
        #print('---')

        # uso un for per analizzare tutte le coppie di annate
        # (ovvero nel caso 1950-1954 => 4 confronti da fare)
        # (1950-1951, 1951-1952, 1952-1953, 1953-1954)
        for i in range(dim - 1):
            y0 = l[i]
            y1 = l[i + 1]

            #print('------------------------------')
            #print(y0)
            #print(y1)
            #print('---')

            m = confronta(time_series, y0, y1)
            #print(m)

            #print('----------')

            anno0 = str(y0)
            anno1 = str(y1)
            anno = anno0 + '-' + anno1
            dMed[anno] = m

        return dMed


#==============================
#  Esempio di utilizzo
#==============================

mio_file = CSVTimeSeriesFile(name='esame/taad.csv')
time_series = mio_file.get_data()

print()

#print(confronta(time_series, 1950, 1951))
print(compute_increments(time_series, '1948', '1956'))
#print(spezzaYear(time_series, 1950))
#print(check(time_series, 1949))
#print(inCSV(time_series, 1950))
#print('Nome del file: "{}"'.format(mio_file.name))
#print('Dati contenuti nel file: \n"{}"'.format(mio_file.get_data()))
#mio_file.get_data()
#print(ordinato(time_series))
#mio_file_numerico = NumericalCSVFile(name='shampoo_sales.csv')
#print('Nome del file: "{}"'.format(mio_file_numerico.name))
#print('Dati contenuti nel file: "{}"'.format(mio_file_numerico.get_data()))
