import numpy as np
import json
from liczenie_energii import Energies
from symulacja import oblicz_przyspieszenia, symuluj_krok
   
# def oblicz_przyspieszenia(masy, x, y, G, wygladzanie=0.01):
#     '''
#     Oblicza przyspieszenia dla trzech ciał.
    
#     Parametry:
#     - masy: lista [m0, m1, m2]
#     - x: lista [x0, x1, x2]
#     - y: lista [y0, y1, y2]
#     - G: stała grawitacyjna
#     - wygladzanie: mała liczba (żeby nie dzielić przez zero)
    
#     Zwraca:
#     - ax, ay: listy przyspieszeń dla każdego ciała
#     '''
    
#     # Na początku wszystkie przyspieszenia zerowe
#     ax = [0.0, 0.0, 0.0]
#     ay = [0.0, 0.0, 0.0]

#     # Liczymy przyspieszenia dla każdej pary ciał
#     for i in range(3):      # i = ciało, na które działa siła (1)
#         for j in range(3):  # j = ciało, które przyciąga (2)
#             if i != j: 
#                 # Wektor od ciała i do ciała j
#                 dx = x[j] - x[i]
#                 dy = y[j] - y[i]

#                 # Długość wektora między ciałami (Pitagoras)
#                 r = np.sqrt(dx*dx + dy*dy) 

#                 # Zabezpieczenie przed dzieleniem przez zero
#                 if r < wygladzanie:
#                     r = wygladzanie
                
#                 # Wartość przyspieszenia
#                 a = G * masy[j] / (r * r)
                
#                 # Dodajemy przyspieszenie do ciała i (z kierunkiem)
#                 ax[i] += a * dx / r
#                 ay[i] += a * dy / r
    
#     return ax, ay


# def symuluj_krok(masy, x, y, vx, vy, G, dt, wygladzanie=0.01):
#     '''
#     Wykonuje 1 krok symulacji.
    
#     Zwraca nowe x, y, vx, vy
#     '''
    
#     # 1. Funkcja "oblicz przyspieszenia" dla danych pozycji
#     ax, ay = oblicz_przyspieszenia(masy, x, y, G, wygladzanie)
    
#     # 2. Zaktualizowanie prędkości (v = v + a * dt)
#     for i in range(3):
#         vx[i] += ax[i] * dt
#         vy[i] += ay[i] * dt
    
#     # 3. Zaktualizowanie pozycji (p = p + v * dt)
#     for i in range(3):
#         x[i] += vx[i] * dt
#         y[i] += vy[i] * dt
    
#     return x, y, vx, vy

# TEST: aby uruchomic wpisać "python main.py" w terminalu

if __name__ == "__main__":
    
    # Dane testowe (Figura osiem)
    masy = [1.0, 1.0, 1.0] 
    G = 1.0
    dt = 0.01
    
    # Pozycje początkowe
    x = [-0.5, 0.5, 0.0]
    y = [0.0, 0.0, 0.866]
    
    # Prędkości początkowe
    vx = [0.5, -0.5, 0.0]
    vy = [0.5, 0.5, -1.0]
    
    print('PRZED symulacją:')
    for i in range(3):
        print(f'Ciało {i}: x={x[i]:.3f}, y={y[i]:.3f}, vx={vx[i]:.3f}, vy={vy[i]:.3f}')
    
    # Wykonaj 10 kroków symulacji
    for krok in range(10):
        x, y, vx, vy = symuluj_krok(masy, x, y, vx, vy, G, dt)
    
    print('\nPO 10 krokach:')
    for i in range(3):
        print(f'Ciało {i}: x={x[i]:.3f}, y={y[i]:.3f}, vx={vx[i]:.3f}, vy={vy[i]:.3f}')


#GŁÓWNA CZĘŚĆ 
#Wczytanie danych z JSON
try:
    with open('configs.json', 'r', encoding='utf-8') as tekst:
        konfiguracje = json.load(tekst) #zamienia tekst z jsona na słownik w pyhtonie
    print('Wczytano plik configs.json')
except FileNotFoundError: #jeśli wyjdzie ten błąd
    print('Błąd: Nie znaleziono pliku configs.json')
    exit() #wychodzi z programu zeby nie crashował


#Wyświetlenie dostępnych konfiguracji
print('\nDostępne konfiguracje:')
lista_nazw = list(konfiguracje.keys()) #robi liste nazw z kluczy słownika (czyli nazw konfiguracji)
for i, nazwa in enumerate(lista_nazw):
    opis = konfiguracje[nazwa].get('opis', 'brak opisu') #jeśli ma opis to 'opis' jak nie to 'brak opisu'
    print(f'{i+1}. {nazwa} -> {opis}')

#Wybranie konfiguracji
wybrana = lista_nazw[0]  #domyślnie pierwsza konfiguracja
print(f'\nWybrano konfigurację {i+1}. {wybrana}')

#Pobranie danych z wybranej 
konfig = konfiguracje[wybrana]

masy = konfig["masy"]
G = konfig.get("G", 1.0)  #jeśli nie ma G to ustawia 1.0
t_max = konfig.get("t_max", 10.0)  #jeśli nie ma ustawia 10

# Pozycje początkowe 'pozycje'][0] to ciało 0 -> [[-0.5, 0.0] 
x = [konfig['pozycje'][0][0], konfig['pozycje'][1][0], konfig['pozycje'][2][0]]
y = [konfig['pozycje'][0][1], konfig['pozycje'][1][1], konfig['pozycje'][2][1]]

# Prędkości początkowe
vx = [konfig["predkosci"][0][0], konfig["predkosci"][1][0], konfig["predkosci"][2][0]]
vy = [konfig["predkosci"][0][1], konfig["predkosci"][1][1], konfig["predkosci"][2][1]]

# Parametry symulacji
dt = 0.01  # krok czasowy
kroki = int(t_max / dt) 
ek_values = [] # tablica na energie kinetyczne
ep_values = [] # tablica na energie potencjalne
et_values = [] # tablica na energie całkowite


if __name__ == "__main__":
    print(f'Czas symulacji: {t_max} s, krok: {dt} s, liczba kroków: {kroki}\n')

    print('STAN POCZĄTKOWY ')
    for i in range(3):
        print(f'Ciało {i}: m={masy[i]}, x={x[i]:.3f}, y={y[i]:.3f}, vx={vx[i]:.3f}, vy={vy[i]:.3f}')
        

    print('\nUruchamianie symulacji...')

    for krok in range(kroki):
        x, y, vx, vy = symuluj_krok(masy, x, y, vx, vy, G, dt)
        
        E_kin = Energies(masy).energia_kinetyczna(vx, vy)
        ek_values.append(E_kin)
        
        E_pot = Energies(masy).energia_potencjalna(x, y, G)
        ep_values.append(E_pot)

        E_tot = Energies(masy).energia_calkowita(x, y, vx, vy, G)
        et_values.append(E_tot)

    print('\nSTAN KOŃCOWY')
    for i in range(3):
        print(f'Ciało {i}: x={x[i]:.3f}, y={y[i]:.3f}, vx={vx[i]:.3f}, vy={vy[i]:.3f}')

    print('\nSymulacja zakończona')