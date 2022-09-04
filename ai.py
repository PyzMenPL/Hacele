import numpy as np
import gra, random

class Ai():
    def __init__(self, nazwa):
        self.plansza = np.zeros([3,3], dtype="int8")
        self.kolumna = 0
        self.sumaKolumn = [0, 0, 0]
        self.nazwa = nazwa
        self.poziomyTrudnosci = [
                'Łatwy', 
                'Średni', 
                'Trudny', 
                'Nieprzewidywalny'
                ]

    def ruch(self, poziomTrudnosci, przeciwnik):

        rzut = random.randrange(1,7,1)

        if poziomTrudnosci == "Łatwy" or poziomTrudnosci == 0:
            self.zagrajLatwo(rzut, przeciwnik)

        if poziomTrudnosci == "Średni" or poziomTrudnosci == 1:
            self.zagrajSrednio(rzut, przeciwnik)

        if poziomTrudnosci == "Trudny" or poziomTrudnosci == 2:
            self.zagrajTrudno(rzut, przeciwnik)

        if poziomTrudnosci == "Nieprzewidywalny" or poziomTrudnosci == 3:
            self.zagrajNieprzewidzianie(rzut, przeciwnik)

    def zagrajLatwo(self, rzut, przeciwnik):
        mozliwe_kolumny_index = [1,1,1]
        czy_trzy = [0,0,0]

        # Sprawdza czy kolumna jest pełna
        for kolumna_petla in range(0,3):
            for wiersz in range(0,3):
                if self.plansza[wiersz,kolumna_petla] != 0:
                    czy_trzy[kolumna_petla] += 1

        # Zmienia możliwe kolumny w zależności od zapełnienia kolumn
        for i in range(0,3):
            if czy_trzy[i] == 3:
                mozliwe_kolumny_index[i] = 0

        while(True):

            for kolumna_petla in range(0,3):
                for wiersz in range(0,3):
                    # Sprawdza czy nie zaatakujemy gracza
                    if rzut == przeciwnik.plansza[wiersz, kolumna_petla]:
                        mozliwe_kolumny_index[kolumna_petla] = 0

                    # Sprawdza czy nie doda sobie punktów
                    if rzut == self.plansza[wiersz, kolumna_petla]:
                        mozliwe_kolumny_index[kolumna_petla] = 0

            # Jeżeli nie ma żadnej możliwości
            if sum(mozliwe_kolumny_index) == 0:
                
                mozliwe_kolumny_index = [1,1,1]

                # Zmienia możliwe kolumny w zależności od zapełnienia kolumn
                for i in range(0,3):
                    if czy_trzy[i] == 3:
                        mozliwe_kolumny_index[i] = 0

                # Niech pryjorytezuje zdobycie punktu, a nie atak
                for kolumna_petla in range(0,3):
                    for wiersz in range(0,3):
                        if rzut == przeciwnik.plansza[wiersz,kolumna_petla]:
                            mozliwe_kolumny_index[kolumna_petla] = 0

                # Jeżeli musi wykować atak to atakuje najkorzystniej dla gracza
                if sum(mozliwe_kolumny_index) == 0:

                    kolumny = [0,0,0]    

                    for kolumna_petla in range(0,3):
                        for wiersz in range(0,3):
                            if rzut == przeciwnik.plansza[wiersz,kolumna_petla]:
                                kolumny[kolumna_petla] += 1
                    
                    # Jeżeli gracz nigdzie nie ma takiej liczby
                    if sum(kolumny) == 0:
                        kolumna = random.randrange(0,3,1)

                    else:
                        najmniejsza = 5

                        for i in range(0,3):
                            if czy_trzy[i] == 3:
                                kolumny[i] = 0

                        mki = []
                        
                        for i in kolumny:
                            if i < najmniejsza and i != 0:
                                najmniejsza = i

                        # Sprawdza czy nie mamy więcej minimalnych
                        if kolumny.count(najmniejsza) > 1:
                            for i in kolumny:
                                if i == najmniejsza:
                                    mki.append(kolumny.index(i))

                        # Jeżeli jest jedna
                        else:
                            mki.append(kolumny.index(najmniejsza))

                        while(True):
                            kolumna = random.randrange(0,3,1)

                            if kolumna in mki:
                                break

                else:
                    while(True):
                        kolumna = random.randrange(0,3,1)

                        if mozliwe_kolumny_index[kolumna] == 1:
                            break
            
            # Jeżeli jest jedna możliwość
            elif sum(mozliwe_kolumny_index) == 1:
                kolumna = mozliwe_kolumny_index.index(1)

            # Jeżeli jest więcej niż jedna możliwość
            else:
                while(True):
                    kolumna = random.randrange(0,3,1)

                    if mozliwe_kolumny_index[kolumna] == 1:
                        break
            
            if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                break
            
    def zagrajSrednio(self, rzut, przeciwnik):
        """Gra pod punkty"""
        while(True):
            zbior_liczb = [0,0,0]
                
            for kolumna_petla in range(0,3):
                for wiersz in range(0,3):
                    if self.plansza[wiersz,kolumna_petla] == rzut:
                        zbior_liczb[kolumna_petla] += 1

            zakres = [2,1,0]

            for kolumna_petla in range(0,3):
                czy_pelna = 0
                for wiersz in zakres:
                    if self.plansza[wiersz,kolumna_petla] != 0:
                        czy_pelna += 1
                if czy_pelna == 3:
                    zbior_liczb[kolumna_petla] = 0
            
            if zbior_liczb[0] == 0 and zbior_liczb[1] == 0 and zbior_liczb[2] == 0:
                kolumna = random.randrange(0,3,1)
               
                if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                    break
                else:
                    continue
                            
            maksymalna = zbior_liczb.index(max(zbior_liczb))
            zbior_liczb[zbior_liczb.index(max(zbior_liczb))] = 0
            
            if maksymalna not in zbior_liczb:
                kolumna = maksymalna

                if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                    break
                else:
                    continue

            else:
                # Jeżeli będą dwie
                maksymalne_indeksy = []
                maksymalne_indeksy.append(zbior_liczb.index(max(zbior_liczb)))
                zbior_liczb[maksymalne_indeksy[0]] = 0
                maksymalne_indeksy.append(zbior_liczb.index(max(zbior_liczb)))
                zbior_liczb[maksymalne_indeksy[1]] = 0
                    
                # Jeżeli będą trzy
                if max(zbior_liczb) == maksymalna:
                    maksymalne_indeksy.append(zbior_liczb.index(max(zbior_liczb)))
                    zbior_liczb[maksymalne_indeksy[2]] = 0                

                # Losuje jedną z kolumn z maksymalną wartością
                while(True):
                    kolumna = random.randrange(0,3,1)
                    if kolumna not in maksymalne_indeksy:
                        continue
                    else:
                        break
            
            if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                break
            else:
                continue

    def zagrajTrudno(self, rzut, przeciwnik):
        kolumna = 0
        mozliwe_kolumny_index = []

        # Jeżeli przeciwnik ma w kolumnie parę liczb >= 3
        male_liczby = ['1','2']
        for kolumna_petla in range(0,3):
            lista_liczb = []
            ile_liczb = {}
            
            # Lista liczb znajdujących się w kolumnie
            for wiersz in range(0,3):
                lista_liczb.append(przeciwnik.plansza[wiersz, kolumna_petla])
            
            # Zapisujemy ile jest unikatowych liczb
            for i in range(1,7):
                if i in lista_liczb:
                    ile_liczb[str(i)] = lista_liczb.count(i)

            for key, value in ile_liczb.items():
                # Jeżeli kolumnę przeciwnika opłaca się atakować to atakuje
                if value >= 2 and key not in male_liczby:
                    mozliwe_kolumny_index.append(kolumna_petla)

        # Po sprawdzeniu wszystkich kolumn wybiera jedną
        if len(mozliwe_kolumny_index) == 1:
            kolumna = mozliwe_kolumny_index[0]
        
        elif len(mozliwe_kolumny_index) > 1:
            while(True):

                kolumna = random.randrange(0,3,1)
                if kolumna in mozliwe_kolumny_index:
                    if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                        break
                    else:
                        continue        
        
        # Jeżeli nie może zaatakować, gra pod punkty
        elif len(mozliwe_kolumny_index) == 0:
            self.zagrajSrednio(rzut, przeciwnik)

    def zagrajNieprzewidzianie(self, rzut, przeciwnik):
        while(True):
            kolumna = random.randrange(0,3,1)

            if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                break
            else:
                continue
