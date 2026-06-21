import argparse
import json

from animacja_panel import AnimacjaPanel

if __name__ == '__main__':
       
    # Żeby użytkownik mógł podać własne parametry
    parser = argparse.ArgumentParser(description = 'Symulacja problemu 3 ciał.')

    parser.add_argument('--config', type = str, default = 'configs.json')
    parser.add_argument('--G', type = float, default = None, help = 'Stała grawitacji (domyślnie z konfiguracji)')
    parser.add_argument('--t_max', type = float, default = None, help = 'Czas symulacji (domyślnie z konfiguracji)')
    parser.add_argument('--dt', type = float, default = 0.01, help = 'Krok czasowy (domyślnie 0.01 s)')
    
    parser.add_argument('--masy', nargs = 3, type = float, default = None, help = 'Masy trzech ciał, np. --masy 1.0 2.0 3.0')
    parser.add_argument('--pozycje', nargs = 6, type = float, default = None, help = 'Pozycje początkowe (x0 y0 x1 y1 x2 y2), np. --pozycje -0.5 0.0 0.5 0.0 0.0 0.5')
    parser.add_argument('--predkosci', nargs = 6, type = float, default = None, help = 'Prędkości początkowe (vx0 vy0 vx1 vy1 vx2 vy2), np. --predkosci 0.0 -0.5 0.0 0.5 0.5 0.0')
    
    parser.add_argument('--kolor', nargs = 9, type = int, default = None, help = 'Kolory ciał RGB, np. r0 g0 b0 r1 g1 b1 r2 g2 b2 (każda wartość 0-255)')
    # parser.add_argument('--nazwa', type = str, default = '', help = 'Nazwa konfiguracji')
    
    args = parser.parse_args()
    
    try: # wyłapywanie, czy plik istnieje
        with open(args.config, 'r') as file:
            configs = json.load(file)
    except FileNotFoundError:
        print(f'Błąd: Nie znaleziono pliku {args.config}')
        exit()

    symulacje = []

    for config in configs.values(): 

        try: # wyłapywanie błędów w konfiguracji
            G = args.G if args.G is not None else config.get('G', 1.0)
            t_max = args.t_max if args.t_max is not None else config.get('t_max', 10.0)
            dt = args.dt if args.dt is not None else config.get('dt', 0.01)
            
            if args.masy is not None:
                masy = args.masy
            else:
                masy = config['masy']

            if any(m <= 0 for m in masy):
                raise ValueError('Masy muszą być > 0!')
                
            if args.pozycje is not None: # sprawdzamy, czy uzytkownik podał własne pozycje
                pozycje = args.pozycje
                x = [pozycje[0], pozycje[2], pozycje[4]]
                y = [pozycje[1], pozycje[3], pozycje[5]]
            else:
                x = [p[0] for p in config['pozycje']]
                y = [p[1] for p in config['pozycje']]

            if args.predkosci is not None: # sprawdzamy, czy uzytkownik podał własne prędkości
                predkosci = args.predkosci
                vx = [predkosci[0], predkosci[2], predkosci[4]]
                vy = [predkosci[1], predkosci[3], predkosci[5]]
            else:
                vx = [v[0] for v in config['predkosci']]
                vy = [v[1] for v in config['predkosci']]

            if G <= 0 or t_max <= 0 or dt <= 0: # sprawdzenie poprawności parametrów
                raise ValueError('Parametry (G, t_max, dt) muszą być > 0!')
            
            if args.kolor is not None:
                colors = [(args.kolor[0], args.kolor[1], args.kolor[2]), 
                          (args.kolor[3], args.kolor[4], args.kolor[5]), 
                          (args.kolor[6], args.kolor[7], args.kolor[8])
                          ]
            else:
                print('Nie podano kolorów, używane będą domyślne.')
                colors = config.get('kolor',[
                    (116,148,196), 
                    (106,77,97), 
                    (195,212,7)
                ])
                

            symulacje.append({
                'masy': masy,
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,

                'G': G,
                't_max': t_max,
                'dt': dt,
                'nazwa': config.get('opis', ''),
                
                'kolor': colors
            })
            
        except ValueError as e: 
            print(f'Błąd w wartości parametru: {e}')
            exit()
        except (ValueError, KeyError, TypeError) as e:
            print(f'Błąd w konfiguracji: {e}')
            print('Spróbuj ponownie wpisać poprawne parametry. ')
            break   
    
    if not symulacje: # niepokazanie symulacji w przypadku błędów w konfiguracji
        exit()
        
    panel = AnimacjaPanel()
    panel.run_all(symulacje)
    