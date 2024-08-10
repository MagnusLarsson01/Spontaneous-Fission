"""
module for spontaneous fission material 

Magnus Larsson 2024
"""
import math
import re
from nuclide import Nuclide
from sfr import SpontaneousFissionResult

class Material():
    """
    A class used to represent a material.
    List of default nuclides: Th232, U232, U233, U234, U235, U236, U238, Np237, 
    Pu236, Pu238, Pu239, Pu240, Pu241, Pu242, Am241, Cm242, Cm244, Cm246, Cm248, 
    Bk249, Cf246, Cf250, Cf252, Cf254, Fm257, No252.

    Parameters
    ----------

    Attributes
    ----------

    """
    def __init__(self):
        self.density = None
        self.nuclide_data = dict()
        self.load_nuclide_data()
        self.material_data = dict()

    def load_nuclide_data(self):
        with open('../data/nuclides.csv') as file:
            first = True
            for row in file:
                if not first:
                    parts = row.split(',')        
                    half_life = math.inf if parts[5] == 'inf' else float(parts[5])
                    self.nuclide_data[parts[0]+parts[2]] = Nuclide(parts[0],parts[0]+parts[2],int(parts[1]),int(parts[2]),float(parts[3]),half_life)
                first = False

    def add_nuclide(self, name, fraction):
       nuclide = self.nuclide_data[name]        
       self.material_data[nuclide] = fraction

    def set_density(self, density_unit, density):
        self.density_unit = density_unit
        self.density = density

    def set_volume(self, volume_unit, volume):
        self.volume_unit = volume_unit
        self.volume = volume

    def calculate_fission_rate(self):
        fission_rates = []
        total = 0.0
        for nuclide, fraction in self.material_data.items():
            total += fraction*nuclide.A
            fission_rates.append(nuclide.get_decay_rate(1)*fraction*nuclide.A)

        fission_rate = sum([x/total for x in fission_rates])
        # print(fission_rate*self.density*self.volume)
        return fission_rate*self.density*self.volume

    def getSFR(self):
        fission_rate = self.calculate_fission_rate()
        sfr = SpontaneousFissionResult(fission_rate, 'fission/second')
        return sfr

    def __repr__(self):
        return "Todo"
    
if __name__=="__main__":
    # 1g of U235 should be 0.00563 fissions per Kg per second
    # uo2 = Material()
    # uo2.add_nuclide('U235', 0.04)
    # uo2.add_nuclide('U238', 0.96)
    # uo2.add_nuclide('O16', 2.0)
    # uo2.set_density('g/cm3', 10.5)
    # uo2.set_volume('cm3', 100)

    # 1g of U235 should be 0.00563 fissions per Kg per second
    # uo2 = Material()
    # uo2.add_nuclide('U238', 1.0)
    # # uo2.add_nuclide('U235', 1.0)
    # uo2.set_density('g/cm3', 18.95)
    # uo2.set_volume('cm3', 0.0528)

    # 1kg of Pu239 should be 0.00563 fissions per Kg per second
    uo2 = Material()
    uo2.add_nuclide('Pu238', 1.0)
    # uo2.add_nuclide('U235', 1.0)
    uo2.set_density('g/cm3', 19.86)
    uo2.set_volume('cm3', 0.0504)

    sfr = uo2.getSFR()
    print(sfr)
