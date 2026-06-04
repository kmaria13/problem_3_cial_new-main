import numpy as np

def oblicz_przyspieszenia(masy, x, y, G, wygladzanie = 0.01): # funkcja do obliczania przyspieszeń
    '''
    Oblicza przyspieszenia dla trzech ciał.
    
    Parametry:
    - masy: lista [m0, m1, m2]
    - x: lista [x0, x1, x2]
    - y: lista [y0, y1, y2]
    - G: stała grawitacyjna
    - wygladzanie: mała liczba (żeby nie dzielić przez zero)
    
    Zwraca:
    - ax, ay: listy przyspieszeń dla każdego ciała
    '''
    
    # Na początku wszystkie przyspieszenia zerowe
    ax = [0.0, 0.0, 0.0]
    ay = [0.0, 0.0, 0.0]

    # Liczymy przyspieszenia dla każdej pary ciał
    for i in range(3):      # i = ciało, na które działa siła (1)
        for j in range(3):  # j = ciało, które przyciąga (2)
            if i != j: 
                # Wektor od ciała i do ciała j
                dx = x[j] - x[i]
                dy = y[j] - y[i]

                # Długość wektora między ciałami (Pitagoras)
                r = np.sqrt(dx*dx + dy*dy) 

                # Zabezpieczenie przed dzieleniem przez zero
                if r < wygladzanie:
                    r = wygladzanie
                
                # Wartość przyspieszenia
                a = G * masy[j] / (r * r)
                
                # Dodajemy przyspieszenie do ciała i (z kierunkiem)
                ax[i] += a * dx / r
                ay[i] += a * dy / r
    
    return ax, ay

def symuluj_krok(masy, x, y, vx, vy, G, dt, wygladzanie=0.01):
    '''
    Wykonuje 1 krok symulacji.
    
    Zwraca nowe x, y, vx, vy
    '''
    
    # 1. Funkcja "oblicz przyspieszenia" dla danych pozycji
    ax, ay = oblicz_przyspieszenia(masy, x, y, G, wygladzanie)
    
    # 2. Zaktualizowanie prędkości (v = v + a * dt)
    for i in range(3):
        vx[i] += ax[i] * dt
        vy[i] += ay[i] * dt
    
    # 3. Zaktualizowanie pozycji (p = p + v * dt)
    for i in range(3):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
    
    return x, y, vx, vy