Problem Trzech Ciał - Symulacja 2D
Autorzy
[Maja] – podstawa symulacji, GUI, animacja, JSON
[Maria] – obsługa błędów, argparse, liczenie energii (całkowitej, kinetycznej, potencjalnej) układu
[Paulina] – część rozszerzona
Co to za program?
Program symuluje ruch trzech ciał, które przyciągają się grawitacyjnie (jak Ziemia, Księżyc i Słońce).
Użytkownik może:

ustawić masy, pozycje i prędkości trzech ciał
wybrać gotową konfigurację z listy
uruchomić animację i obserwować trajektorie
zatrzymać, zresetować i eksperymentować z parametrami
Jak uruchomić?
Krok 1: Instalowanie wymaganych bibliotek
Otwórz terminal (konsolę) i wpisz:

pip install numpy scipy matplotlib PySide6

Plik configs.json
Plik przechowuje gotowe konfiguracje układów trzech ciał w formacie JSON, z których użytkownik może potem korzystać.

Struktura:

Klucz główny: nazwa konfiguracji
W środku: opis co to za konfiguracja, masy, pozycje, prędkości, G, czas symulacji
Jak dodać własną konfigurację:

Otwórz configs.json w notatniku
Dodaj nowy wpis przed ostatnią klamrą
Użyj podwójnych cudzysłowów i przecinków między elementami
Zapisz plik i uruchom program
