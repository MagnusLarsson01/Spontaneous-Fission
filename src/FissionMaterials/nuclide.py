import math

class Nuclide():

    def __init__(self,element, name, Z, A, molar_mass, sf_half_life, half_life_unit='y', density=1.0):
        self.element = element
        self.name = name
        self.Z = Z
        self.A = A
        self.molar_mass = molar_mass
        self.sf_half_life = sf_half_life
        self.density = density
        self.half_life_unit = half_life_unit

    def get_nuclide_notation(self):
        return self.Z*1000 + self.A
    
    def get_lambda(self):
        if self.half_life_unit == 'y':
            return  math.log(2)/(self.sf_half_life*365*24*3600) # s

    def get_decay_rate(self, mass, unit='g'):
        if unit=='g':
            N = mass/self.molar_mass*6.022E23
            return self.get_lambda()*N