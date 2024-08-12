import math

class Nuclide():
    """
    A class used to represent a given nucleotide.
    The class also contain functions for calculation of lambda and decay rate.

    Parameters
    ----------
    element : str
        Element name e.g. U
    name : str
        Name of nuclide e.g. U238
    Z : int
        Atomic number e.g. 92 for Uranium
    A : int
        Mass number e.g 238 for U238
    molar_mass : float
        The molar mass fo the isotope g/mol
    sf_half_life : float
        Half life based on spontaneous fission
    half_life_unit : float
        Unit for the half life y (year, default), d (days)
    density : float
        Density of the pure isotope g/cm-3
        
    Attributes
    ----------
    element : str
        Element name e.g. U
    name : str
        Name of nuclide e.g. U238
    Z : int
        Atomic number e.g. 92 for Uranium
    A : int
        Mass number e.g 238 for U238
    molar_mass : float
        The molar mass fo the isotope g/mol
    sf_half_life : float
        Half life based on spontaneous fission
    half_life_unit : float
        Unit for the half life y (year, default), d (days)
    density : float
        Density of the pure isotope g/cm-3

    """
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
        return str(self.Z*1000 + self.A)
    
    def get_lambda(self):
        if self.half_life_unit == 'y':
            return  math.log(2)/(self.sf_half_life*365*24*3600) # s

    def get_decay_rate(self, mass, unit='g'):
        if unit=='g':
            N = mass/self.molar_mass*6.022E23
            return self.get_lambda()*N