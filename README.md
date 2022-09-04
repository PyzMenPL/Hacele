# Hacele

## Na czym polega gra?

W hacele gra się w dwóch graczy. Każdy gracz ma planszę na której znajdują się trzy kolumny, każda z trzema miejscami na kości. Na początku gry losowo zostaje wybrany jeden z graczy który pierwszy rzuca kością, następnie wynik swojego rzutu musi umieścić w jednej z trzech kolumn i oddać kość swojemu przeciwnikowi.

Gra trwa aż jeden z graczy nie zapełni sowjej planszy. Gdy do tego dojdzie sumuje się zdobyte punkty z poszczególnych kolumn (jedno oczko = jeden punkt). Gracz z większą liczbą punktów wygrywa.

Jeżeli gracz umieści  w jednej z kolumn kilka tych samych liczb, ich suma zostaje podwojona, na przykład: jeżeli w kolumnie mam: 2; 3 i 2, to suma tej kolumny wynosi 11, ponieważ: (2+2) * 2 + 3; jeżeli w kolumnie mam same trójki, to mój wynik jest równy 18, ponieważ (3 + 3 + 3) * 2.

Gracze mogą sobie przeszkadzać. Załóżmy taką sytuacje: nasz przeciwnik ma w pierwszej kolumnie: 1; 1 oraz 5, a my wyrzuciliśmy kością jeden, jeżeli postawimy tą jedynkę w naszej pierwszej kolumnie to wtedy wszystkie takie same wartości z równoległej kolumny przeciwnika znikają, czyli teraz zamiast mieć w kolumnie: 1; 1; 5; ma on tylko 5.

# Jak kożystać z gry?

Gra działa na razie tylko na Linuksie! Jest to spowodowane biblioteką simple-term-menu.

Wymagane są numpy oraz simple-term-menu:

```bash
python3 -m pip install numpy
```
```bash
python3 -m pip install simple-term-menu
```

Aby uruchomić: 
```bash
python3 main.py
```
