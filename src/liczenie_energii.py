class Energies:
    def __init__(self, masy):
        self.masy = masy
        
    # funkcja do liczenia energii kinetycznej
    def energia_kinetyczna(self, vx, vy):
        E_kin = 0.0
        return sum(0.5 * self.masy[i] * (vx[i]**2 + vy[i]**2) for i in range(3))
    
    # funkcja do liczenia energii potencjalnej
    def energia_potencjalna(self, x, y, G):
        E_pot = 0.0
        for i in range(3):
            for j in range(i + 1, 3):
                dx = x[j] - x[i] # różnica x
                dy = y[j] - y[i] # różnica y
                r = (dx**2 + dy**2)**0.5 # odległość między ciałami
                E_pot -= G * self.masy[i] * self.masy[j] / r # energia potencjalna
                
        return E_pot
    
    def energia_calkowita(self, x, y, vx, vy, G):
        E_tot = 0.0
        for i in range(3):
            E_tot = self.energia_kinetyczna(vx, vy) + self.energia_potencjalna(x, y, G)
        return E_tot
        
    