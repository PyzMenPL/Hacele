###############################################################################
# TO DO:
# 
# 1. Menu:
#   - Gra na ślepo - nie widzisz planszy przeciwnika
#   - Logi gry - każdy ruch zostaje zapisany
#   - Podpowiedzi - gra może podpowiadać następne dobre zagranie
#   - Widać % szans na wyrzucenie konkretnej liczby
#   - Tablica z wynikami ostatnich gier
#   - Możliwość zmiany trybu wybierania kolumny z liczb na strzałki
#   - Zmiana ikony wskaźnika (Graj, instrukcja, opcje, wyjście) na dowolną
#   - Zmiana obramowania plansz
#
# 2. Optymalizacja
# 3. Zastąpić simple_term_menu curses i sprawdzić czy wogóle się opłaca (https://stackoverflow.com/questions/39488788/how-to-make-a-menu-in-python-navigable-with-arrow-keys)
# 4. Obsługa wielu języków
# 5. Efekty dźwiękowe
###############################################################################

import numpy as np
import random, os, time, json
from simple_term_menu import TerminalMenu

import gra
      
# Zmienne
gra = gra.Gra()

menuGlowne = TerminalMenu(["Graj", "Instrukcja", "Opcje", "Wyjście"])
menuPrzeciwnika = TerminalMenu(["Gra przeciwko komputerowi", "Gra lokalna"])
menuTrudnosci = TerminalMenu(["Łatwy", "Średni", "Trudny", "Nieprzewidywalny"])
menuInstrukcji = TerminalMenu(["Rozumiem!"])
menuPoGrze = TerminalMenu(["Zagraj ponownie", "Powrót"])
menuOpcje = TerminalMenu(gra.konfiguracja.keys(),
            multi_select=True,
            multi_select_select_on_accept=False,
            multi_select_empty_ok=True,
            preselected_entries=gra.konfiguracjaWybrane,
            )

# Główna pętla gry
while(True):
    os.system('cls' if os.name == 'nt' else 'clear')
    gra.hacele()

    menuEntryIndex = menuGlowne.show()

    # Graj
    if menuEntryIndex == 0:
        print("Wybierz tryb gry:\n")
        menuEntryIndex1 = menuPrzeciwnika.show()
       
        try:
            int(menuEntryIndex1)
        except TypeError:
            continue
        
        poziomTrudnosci = -1
        # Gra z komputerem
        if menuEntryIndex1 == 0:
            gracz = gra.stworzGracza("Gracz")
            przeciwnik = gra.stworzAi("AI")

            poziomTrudnosci = menuTrudnosci.show()

            try:
                int(poziomTrudnosci)
            except TypeError:
                continue

        # Gra lokalna
        elif menuEntryIndex1 == 1:
            gracz = gra.stworzGracza("Gracz 1")
            przeciwnik = gra.stworzGracza("Gracz 2")

        # Kto pierwszy
        czyGracz = True
        czyPierwszy = False
        kolej = random.randrange(0, 2, 1)
        
        # Gracz gra pierwszy
        if kolej == 0:
            gra.formalnosci(gracz, przeciwnik, poziomTrudnosci)
            print("Zaczyna " + gracz.nazwa + '\n')
            gracz.ruch(przeciwnik)
            czyGracz = False

        # Przeciwnik gra pierwszy
        else:
            gra.formalnosci(przeciwnik, gracz, poziomTrudnosci)

            if przeciwnik.nazwa == 'AI':
                przeciwnik.ruch(poziomTrudnosci, gracz)
            else:
                print("Zaczyna " + przeciwnik.nazwa + '\n')
                przeciwnik.ruch(gracz)
                 
            czyGracz = True

        while(True):
            # Sprawdzanie jaki jest wynik gry
            if 0 not in gracz.plansza or 0 not in przeciwnik.plansza:
                if sum(gracz.sumaKolumn) > sum(przeciwnik.sumaKolumn):
                    gra.formalnosci(gracz, przeciwnik, poziomTrudnosci)
                    print("Wygrał " + gracz.nazwa + "!\n")

                elif sum(gracz.sumaKolumn) < sum(przeciwnik.sumaKolumn):
                    if przeciwnik.nazwa == "AI":
                        gra.formalnosci(gracz, przeciwnik, poziomTrudnosci)
                    else:
                        gra.formalnosci(przeciwnik, gracz, poziomTrudnosci)
                    
                    print("Wygrał " + przeciwnik.nazwa + "!\n")

                else:
                    print("Remis!")
                
                poGrzeIndex = menuPoGrze.show()

                # Zagraj ponownie
                if poGrzeIndex == 0:
                    gracz.plansza = np.zeros([3,3], dtype="int8")
                    przeciwnik.plansza = np.zeros([3,3], dtype="int8")
                    kolej = random.randrange(0, 2, 1)
                    czyPierwszy = True
                    continue

                # Powrót
                if poGrzeIndex == 1:
                    break

            # Jeżeli jest kolej gracza
            if czyGracz == True:
                gra.formalnosci(gracz, przeciwnik, poziomTrudnosci)
                if czyPierwszy:
                    print("Zaczyna " + gracz.nazwa + '\n')   
                    czyPierwszy = False
                gracz.ruch(przeciwnik)
                czyGracz = False

            # Jeżeli jest kolej przeciwnika
            else:
                gra.formalnosci(przeciwnik, gracz, poziomTrudnosci)

                if przeciwnik.nazwa == 'AI':
                    przeciwnik.ruch(poziomTrudnosci, gracz)
                else:
                    if czyPierwszy:
                        print("Zaczyna " + przeciwnik.nazwa + '\n')
                        czyPierwszy = False
                    przeciwnik.ruch(gracz)
                 
                czyGracz = True
            
    # Instrukcja
    if menuEntryIndex == 1:
        print("""W hacele gra się w dwóch graczy. Każdy gracz ma planszę
na której znajdują się    trzy kolumny, każda z  trzema
miejscami   na  kości. Na początku   gry losowo zostaje
wybrany    jeden z  graczy który pierwszy rzuca kością,
następnie    wynik swojego rzutu musi umieścić w jednej
z  trzech  kolumn i  oddać  kość swojemu przeciwnikowi.

Gra trwa aż  jeden z graczy nie zapełni sowjej planszy.
Gdy  do    tego    dojdzie sumuje    się zdobyte punkty
z   poszczególnych  kolumn (jedno oczko = jeden punkt).
Gracz z większą liczbą punktów wygrywa.

Jeżeli gracz      umieści  w jednej z kolumn kilka tych
samych liczb, ich suma zostaje podwojona,  na przykład:
jeżeli    w kolumnie mam: 2; 3 i 2, to suma tej kolumny
wynosi  11, ponieważ: (2+2) * 2 + 3;  jeżeli w kolumnie
mam same trójki,  to mój wynik jest  równy 18, ponieważ
(3 + 3 + 3) * 2.

Gracze      mogą sobie      przeszkadzać.  Załóżmy taką
sytuacje:    nasz  przeciwnik  ma w pierwszej kolumnie:
1;   1  oraz 5, a  my wyrzuciliśmy kością jeden, jeżeli
postawimy    tą jedynkę w naszej  pierwszej kolumnie to
wtedy       wszystkie takie same wartości z równoległej
kolumny  przeciwnika znikają,  czyli teraz zamiast mieć
w kolumnie: 1; 1; 5; ma tylko 5.\n""")

        menuEntryIndex = menuInstrukcji.show()

        try:
            if menuEntryIndex == 0:
                continue
        except TypeError:
            continue
    # Opcje
    if menuEntryIndex == 2:
        print("Zaznacz -> spacja\nZapisz -> enter\n")

        while(True):
            wyborOpcje = menuOpcje.show()

            # Jeżeli wcisnę enter bez zaznaczenia czegoś pokazuje się TypeError
            try:
                len(wyborOpcje)

            except TypeError:
                for key in gra.konfiguracja.keys():
                    gra.konfiguracja[key] = False
                break
            
            else:
                """
                Obsługa gry strzałkami:


                Propozycja nr 1:

                Plansza Gracza:

                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
                ^
                (Można zmienić styl strzałki :D)
                ================
                Propozycja nr 2:
                
                Plansza Gracza:

                ██0██▏ 0 ▕▏ 0 ▕▏
                ██0██▏ 0 ▕▏ 0 ▕▏
                ██0██▏ 0 ▕▏ 0 ▕▏
                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    
                (Zmiana koloru tła)
                ===================
                Propozycja nr 3:

                Plansza Gracza:

                ∇
                
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
                ∆
                (Strzałki po obu stronach)
                (Ten trójkącik podoba mi się bardziej niż strzałka)
                ====================
                Propozycja nr 4:

                Plansza Gracza:

                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
                ▷  Kolumna 1
                Kolumna 2
                Kolumna 3

                (Menu)
                ====================            
                Propozycja nr 5:

                Plansza Gracza:

                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▕▏ 0 ▕▏ 0 ▕▏ 0 ▕▏
                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
                Wybierz kolumnę (1-3):

                (To co jest ale bez potwierdzania enterem)
                """
                if 0 in wyborOpcje:
                    gra.konfiguracja["Tryb w ciemno"] = True
                else:
                    gra.konfiguracja["Tryb w ciemno"] = False

                # Zrobione
                if 1 in wyborOpcje:
                    gra.konfiguracja["Wymaż napis hacele po wyjściu z gry"] = True
                else:
                    gra.konfiguracja["Wymaż napis hacele po wyjściu z gry"] = False

                # Zrobione
                if 2 in wyborOpcje:
                    gra.konfiguracja["Ustaw plansze obok siebie"] = True
                else:
                    gra.konfiguracja["Ustaw plansze obok siebie"] = False
                               
                if gra.konfiguracja["Tryb w ciemno"] == True and gra.konfiguracja["Ustaw plansze obok siebie"] == True:
                    gra.konfiguracja["Tryb w ciemno"] = True
                    gra.konfiguracja["Ustaw plansze obok siebie"] = False
                
                with open("konfiguracja.json", 'w') as file:
                    json.dump(gra.konfiguracja, file)

                break
    # Wyjście
    if menuEntryIndex == 3:
        if gra.konfiguracja["Wymaż napis hacele po wyjściu z gry"] == True:
            os.system('cls' if os.name == 'nt' else 'clear')
        exit()
