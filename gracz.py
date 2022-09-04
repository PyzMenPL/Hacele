import numpy as np
import gra, random

class Gracz():
    def __init__(self, nazwa):
        self.plansza = np.zeros([3,3], dtype="int8")
        self.sumaKolumn = [0, 0, 0]
        self.nazwa = nazwa

    def rzutKoscia(self):
        '''Gracz rzuca kością kością'''
        return random.randrange(1,7,1) 

    def ruch(self, przeciwnik):
        rzut = self.rzutKoscia()
        print("Wyrzuciłeś " + str(rzut))
        
        # Sprawdzenie czy podana przez gracza wartość jest poprawna
        while(True):
            kolumna = input("Wybierz kolumnę (1-3): ")

            try:
                kolumna = int(kolumna) - 1
            except ValueError:
                print("Podana wartość nie jest liczbą!")
                continue
            
            if kolumna < 0 or kolumna > 2:
                print("Podana wartość jest poza zakresem!")
                continue

            if self.plansza[2, kolumna] != 0 and self.plansza[1, kolumna] != 0 and self.plansza[0, kolumna] != 0:
                print("Kolumna jest pełna!")
                continue

            # TO ZADZIAŁAAAAAAAAAAA!!!!!!!!!!! 
            if gra.Gra().postawKosc(self, kolumna, rzut, przeciwnik):
                break
            else:
                continue
