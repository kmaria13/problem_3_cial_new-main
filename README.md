# Problem Trzech Ciał - Symulacja 2D

## Autorki
- Maja – podstawa symulacji, GUI, animacja, JSON.
- Maria – obsługa błędów, argumenty wiersza poleceń (arparse), obliczanie energii: całkowitej, potencjalnej i kinetycznej układu.
- Paulina - tworzenie 3 ciał, PyGame, pobieranie pierwotnych danych pozycyjnych i tworzenie czterech paneli

---

## Co to za program?

Program symuluje ruch trzech ciał, które przyciągają się grawitacyjnie (jak Ziemia, Księżyc i Słońce).  
Użytkownik może:
- ustawić masy, pozycje i prędkości trzech ciał
- wybrać gotową konfigurację z listy
- uruchomić animację i obserwować trajektorie
- zatrzymać, zresetować i eksperymentować z parametrami

---

## Jak uruchomić?

### Krok 1: Instalowanie wymaganych bibliotek

Otwórz terminal (konsolę) i wpisz:

pip install numpy scipy matplotlib PySide6

## Plik configs.json

Plik przechowuje gotowe konfiguracje układów trzech ciał w formacie JSON, z których użytkownik może potem korzystać.

**Struktura:**
- Klucz główny: nazwa konfiguracji
- W środku: opis co to za konfiguracja, masy, pozycje, prędkości, G, czas symulacji

**Jak dodać własną konfigurację:**
1. Otwórz configs.json w notatniku
2. Dodaj nowy wpis przed ostatnią klamrą
3. Użyj podwójnych cudzysłowów i przecinków między elementami
4. Zapisz plik i uruchom program
