import gracz, ai, random, os, json

# Gdy będę chciał wygenerować nowy plik konfiguracyjny
"""
konfig = {"Tryb w ciemno": False,
        "Wymaż napis hacele po wyjściu z gry":False,
        "Ustaw plansze obok siebie":False
        }


with open("konfiguracja.json", 'w') as file:
    json.dump(konfig, file)
"""
class Gra():
    def __init__(self):
        self.konfiguracja = dict()
        with open("konfiguracja.json", "r") as file:
            self.konfiguracja = json.load(file)
        
        self.konfiguracjaWybrane = []
        for key, value in self.konfiguracja.items():
            if value == True:
                self.konfiguracjaWybrane.append(key)

    def stworzGracza(self, nazwa):
        return gracz.Gracz(nazwa)
    
    def stworzAi(self, nazwa):
        return ai.Ai(nazwa) 
    
    def postawKosc(self, gracz, kolumna, rzut, przeciwnik):
        """Ustawia wynik rzutu we wskazanej kolumnie"""
        zakres = [2, 1, 0]
        for i in zakres:
            # Szuka pustego miejsca w swojej kolumnie
            if gracz.plansza[i,kolumna] == 0:
                gracz.plansza[i,kolumna] = rzut

                # Sprawdza jak ruch odbił się na przeciwniku
                for wiersz in zakres:
                    if rzut == przeciwnik.plansza[wiersz,kolumna]:
                        przeciwnik.plansza[wiersz,kolumna] = 0
                #break

                return True
        return False

    def formalnosci(self, gracz1, przeciwnik, poziomTrudnosci):
        """Pozbywa się zer, sumuje kolumny i pokazuje plansze"""
        gracze = [gracz1, przeciwnik]

        zakres = [2, 1]

        
        for gracz in gracze:
            # Pozbycie się zer
            for wiersz in zakres:
                for kolumna in range(0,3):
                    # Jeżeli usunęło się na parterze i jest nad tym
                    if gracz.plansza[wiersz,kolumna] == 0 and gracz.plansza[wiersz-1,kolumna] != 0:
                        gracz.plansza[wiersz,kolumna] = gracz.plansza[wiersz-1,kolumna]
                        gracz.plansza[wiersz-1,kolumna] = 0
                    
                    # Jeżeli usunęło się na parterze i jest nad tym + 1
                    if wiersz == 2 and gracz.plansza[wiersz,kolumna] == 0 and gracz.plansza[wiersz-2,kolumna] != 0:
                        gracz.plansza[wiersz,kolumna] = gracz.plansza[wiersz-2,kolumna]
                        gracz.plansza[wiersz-2,kolumna] = 0

            # Zsumowanie kolumn
            for kolumna in range(0,3):
                pion_org = []
            
                for wiersz in range(0,3):
                    pion_org.append(gracz.plansza[wiersz,kolumna])
            
                pion_fin = pion_org[:]

                # Mnożenie wartości jeżeli liczby by się powtórzyły
                if pion_org[0] == pion_org[1] or pion_org[0] == pion_org[2]:
                    pion_fin[0] = pion_fin[0]*2
                if pion_org[1] == pion_org[0] or pion_org[1] == pion_org[2]:
                    pion_fin[1] = pion_fin[1]*2
                if pion_org[2] == pion_org[1] or pion_org[2] == pion_org[0]:
                    pion_fin[2] = pion_fin[2]*2

                gracz.sumaKolumn[kolumna] = sum(pion_fin)

        self.printPlansze(gracz1, przeciwnik, poziomTrudnosci)
    
    def czyPelna(self, gracz, przeciwnik):
        gracze = [gracz, przeciwnik]

        for gracz in gracze:
            czyPelna = 0
            for wiersz in range(0,3):
                for kolumna in range(0,3):
                    if gracz.plasza[wiersz,kolumna] != 0:
                        czyPelna += 1

            if czyPelna == 9:
                return gracz.nazwa

    def hacele(self):
        """Wypisuje na ekranie napis HACELE"""
        print(""" .S    S.    .S_SSSs      sSSs    sSSs  S.        sSSs  
.SS    SS.  .SS~SSSSS    d%%SP   d%%SP  SS.      d%%SP  
S%S    S%S  S%S   SSSS  d%S'    d%S'    S%S     d%S'    
S%S    S%S  S%S    S%S  S%S     S%S     S%S     S%S     
S%S SSSS%S  S%S SSSS%S  S&S     S&S     S&S     S&S     
S&S  SSS&S  S&S  SSS%S  S&S     S&S_Ss  S&S     S&S_Ss  
S&S    S&S  S&S    S&S  S&S     S&S~SP  S&S     S&S~SP  
S&S    S&S  S&S    S&S  S&S     S&S     S&S     S&S     
S*S    S*S  S*S    S&S  S*b     S*b     S*b     S*b     
S*S    S*S  S*S    S*S  S*S.    S*S.    S*S.    S*S.    
S*S    S*S  S*S    S*S   SSSbs   SSSbs   SSSbs   SSSbs  
SSS    S*S  SSS    S*S    YSSP    YSSP    YSSP    YSSP  
SP          SP                                   
Y           Y\n\n""")

    def printPlansze(self, gracz, przeciwnik, poziomTrudnosci):
        """Pokazuje plansze graczy i ich wynik"""
        os.system('cls' if os.name == 'nt' else 'clear')

        self.hacele()

        poziom = ''

        if poziomTrudnosci == 0 or poziomTrudnosci == "Łatwy":
            poziom = "Łatwy"
        elif poziomTrudnosci == 1 or poziomTrudnosci == "Średni":
            poziom = "Średni"
        elif poziomTrudnosci == 2 or poziomTrudnosci == "Trudny":
            poziom = "Trudny"
        elif poziomTrudnosci == 3 or poziomTrudnosci == "Nieprzewidywalny":
            poziom = 'Nieprzewidywalny'

        if poziomTrudnosci != -1:
            print("Poziom trudności: " + poziom + '\n')


        if self.konfiguracja["Ustaw plansze obok siebie"] == True:

            print(" Plansza " + przeciwnik.nazwa + ":\t\t║\t Plansza " + gracz.nazwa + ":")

            for i in range(0,3):
                print('▕▏ ' + str(przeciwnik.plansza[i,0]) + ' ▕▏ ' + str(przeciwnik.plansza[i,1]) + ' ▕▏ ' + str(przeciwnik.plansza[i,2]) + ' ▕▏\t║\t▕▏ ' + str(gracz.plansza[i,0]) + ' ▕▏ ' + str(gracz.plansza[i,1]) + ' ▕▏ ' + str(gracz.plansza[i,2]) + ' ▕▏')

            print(' ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\t║\t ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔')

            print('   ' + str(przeciwnik.sumaKolumn[0]) + ('  + ' if przeciwnik.sumaKolumn[0] < 10 else ' + ') + str(przeciwnik.sumaKolumn[1]) + ('  + ' if przeciwnik.sumaKolumn[1] < 10 else ' + ') + str(przeciwnik.sumaKolumn[2]) + ('  = ' if przeciwnik.sumaKolumn[2] < 10 else ' = ') + str(sum(przeciwnik.sumaKolumn)) + '\t║\t   ' + str(gracz.sumaKolumn[0]) + ('  + ' if gracz.sumaKolumn[0] < 10 else ' + ') + str(gracz.sumaKolumn[1]) + ('  + ' if gracz.sumaKolumn[1] < 10 else ' + ') + str(gracz.sumaKolumn[2]) + ('  = ' if gracz.sumaKolumn[2] < 10 else ' = ') + str(sum(gracz.sumaKolumn)))

            print('════════════════════════╩═══════════════════════════')

        else:
            if self.konfiguracja["Tryb w ciemno"] == False:
                print("Plansza " + przeciwnik.nazwa + ":\n")

                for i in range(0,3):
                    print('▕▏ ' + str(przeciwnik.plansza[i,0]) + ' ▕▏ ' + str(przeciwnik.plansza[i,1]) + ' ▕▏ ' + str(przeciwnik.plansza[i,2]) + ' ▕▏')

                print(' ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔')

                print('   ' + str(przeciwnik.sumaKolumn[0]) + ('  + ' if przeciwnik.sumaKolumn[0] < 10 else ' + ') + str(przeciwnik.sumaKolumn[1]) + ('  + ' if przeciwnik.sumaKolumn[1] < 10 else ' + ') + str(przeciwnik.sumaKolumn[2]) + ('  = ' if przeciwnik.sumaKolumn[2] < 10 else ' = ') + str(sum(przeciwnik.sumaKolumn)))


                print('════════════════════')

            print("Plansza " + gracz.nazwa + ":\n")

            for i in range(0,3):
                print('▕▏ ' + str(gracz.plansza[i,0]) + ' ▕▏ ' + str(gracz.plansza[i,1]) + ' ▕▏ ' + str(gracz.plansza[i,2]) + ' ▕▏')

            print(' ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔')

            print('   ' + str(gracz.sumaKolumn[0]) + ('  + ' if gracz.sumaKolumn[0] < 10 else ' + ') + str(gracz.sumaKolumn[1]) + ('  + ' if gracz.sumaKolumn[1] < 10 else ' + ') + str(gracz.sumaKolumn[2]) + ('  = ' if gracz.sumaKolumn[2] < 10 else ' = ') + str(sum(gracz.sumaKolumn)) + '\n')
