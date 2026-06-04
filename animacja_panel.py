#chce uzyc pygame do stworzenia panelu animacji, który będzie wyświetlał animację na ekranie
import pygame
import numpy as np
import argparse
import json
from main import oblicz_przyspieszenia, symuluj_krok
from liczenie_energii import Energies
#chcialabym aby robilo animacje w loop czyli gdy sie konczy to wraca od nowa, by nie konczyla sie po jednym kroku, ale zeby mozna bylo zatrzymac i wznowic animacje

with open('configs.json', 'r') as f:
    configs = json.load(f)

class AnimacjaPanel:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Symulacja Trzech Ciał - 4 panele")
        self.clock = pygame.time.Clock()
        self.running = True

        self.width = width
        self.height = height

        self.panel_w = width // 2
        self.panel_h = height // 2

    def draw_bodies(self, sim, offset_x, offset_y):
        colors = [(116,148,196), (106,77,97), (195,212,7)]

        panel_rect = pygame.Rect(offset_x, offset_y, self.panel_w, self.panel_h)

        # ograniczamy rysowanie tylko do tego panelu
        old_clip = self.screen.get_clip()
        self.screen.set_clip(panel_rect)

        x = sim["x"]
        y = sim["y"]
        trails = sim["trails"]

        # ramka panelu
        pygame.draw.rect(self.screen, (70, 70, 70), panel_rect, 2)

        for i in range(3):
            px = int(x[i] * 70 + offset_x + self.panel_w // 2)
            py = int(y[i] * 70 + offset_y + self.panel_h // 2)

            # jeśli punkt wyszedł poza panel, czyścimy ślad tego ciała
            if not panel_rect.collidepoint(px, py):
                trails[i].clear()
                continue

            trails[i].append((px, py))

            if len(trails[i]) > 60:
                trails[i].pop(0)

            if len(trails[i]) > 1:
                pygame.draw.lines(self.screen, colors[i], False, trails[i], 2)

            pygame.draw.circle(self.screen, colors[i], (px, py), 6)

        # przywracamy normalne rysowanie
        self.screen.set_clip(old_clip)
    
    # Wypisywanie energii kinetycznej
    def draw_kinetic_energy(self, sim, offset_x, offset_y):
        font = pygame.font.SysFont("Arial", 16)

        text = font.render(
            f"Energia kinetyczna układu: {sim['energia_kinetyczna']:.3f} J",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (offset_x + 10, offset_y + 10)) # rysujemy tekst w lewym górnym rogu panelu
       
       
    # Wypisywanie energii potencjalnej
    def draw_potential_energy(self, sim, offset_x, offset_y):
        font = pygame.font.SysFont("Arial", 16)

        text = font.render(
            f"Energia potencjalna układu: {sim['energia_potencjalna']:.3f} J",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (offset_x + 10, offset_y + 30)) # rysujemy tekst poniżej energii kinetycznej

    def draw_total_energy(self, sim, offset_x, offset_y):
        font = pygame.font.SysFont("Arial", 16)

        text = font.render(
            f"Energia całkowita układu: {sim['energia_calkowita']:.3f} J",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (offset_x + 10, offset_y + 50)) # rysujemy tekst poniżej energii potencjalnej

    def run_all(self, symulacje):
        paused = False

        # dodajemy dane startowe i ścieżki osobno dla każdej symulacji
        for sim in symulacje:
            sim["start_x"] = sim["x"].copy()
            sim["start_y"] = sim["y"].copy()
            sim["start_vx"] = sim["vx"].copy()
            sim["start_vy"] = sim["vy"].copy()
            sim["trails"] = [[], [], []]
            sim["step_counter"] = 0
            sim["max_steps"] = 440
            sim['energies'] = Energies(sim['masy'])
            sim['energia_kinetyczna'] = 0.0
            sim['energia_potencjalna'] = 0.0
            sim['energia_calkowita'] = 0.0
            
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

            if not paused:
                for sim in symulacje:
                    sim["x"], sim["y"], sim["vx"], sim["vy"] = symuluj_krok(
                        sim["masy"],
                        sim["x"],
                        sim["y"],
                        sim["vx"],
                        sim["vy"],
                        sim["G"],
                        sim["dt"]
                    )
                    
                    sim['energia_kinetyczna'] = sim['energies'].energia_kinetyczna(sim['vx'], sim['vy'])
                    sim['energia_potencjalna'] = sim['energies'].energia_potencjalna(sim['x'], sim['y'], sim['G'])
                    sim['energia_calkowita'] = sim['energies'].energia_calkowita(sim['x'], sim['y'], sim['vx'], sim['vy'], sim['G'])
                    sim["step_counter"] += 1

                    if sim["step_counter"] >= sim["max_steps"]:
                        sim["x"] = sim["start_x"].copy()
                        sim["y"] = sim["start_y"].copy()
                        sim["vx"] = sim["start_vx"].copy()
                        sim["vy"] = sim["start_vy"].copy()
                        sim["trails"] = [[], [], []]
                        sim["step_counter"] = 0

            self.screen.fill((0, 0, 0))

            for index, sim in enumerate(symulacje[:4]):
                col = index % 2
                row = index // 2

                offset_x = col * self.panel_w
                offset_y = row * self.panel_h

                self.draw_bodies(sim, offset_x, offset_y)
                
                self.draw_kinetic_energy(sim, offset_x, offset_y)
                self.draw_potential_energy(sim, offset_x, offset_y)
                self.draw_total_energy(sim, offset_x, offset_y)
                
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
   
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Symulacja problemu 3 ciał.')
    parser.add_argument('--config', type = str, default = 'configs.json')
    parser.add_argument('--G', type = float, default = None, help = 'Stała grawitacji (domyślnie z konfiguracji)')
    parser.add_argument('--t_max', type = float, default = None, help = 'Czas symulacji (domyślnie z konfiguracji)')
    parser.add_argument('--dt', type = float, default = 0.01, help = 'Krok czasowy (domyślnie 0.01 s)')

    args = parser.parse_args()

    try:
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

            if G <= 0 or t_max <= 0 or dt <= 0:
                raise ValueError('Parametry muszą być > 0!')

            symulacje.append({
                'masy': config["masy"],
                'x': [p[0] for p in config["pozycje"]],
                'y': [p[1] for p in config["pozycje"]],
                'vx': [v[0] for v in config["predkosci"]],
                'vy': [v[1] for v in config["predkosci"]],

                'G': G,
                't_max': t_max,
                'dt': dt,
                'nazwa': config.get('opis', '')
            })

        except (ValueError, KeyError, TypeError) as e:
            print(f'Błąd w konfiguracji: {e}')
            print('Spróbuj ponownie wpisać poprawne parametry. ')
            break

    if not symulacje: # niepokazanie symulacji w przypadku błędów w konfiguracji
        exit()
        
    panel = AnimacjaPanel()
    panel.run_all(symulacje)
    