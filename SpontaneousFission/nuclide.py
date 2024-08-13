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
        Unit for the half life y (year, default), d (days), s (seconds)
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
        """
        The function calculates the decay constant lambda.
        
        Returns
        -------
        float
            the decay constant lambda
        """
        if self.half_life_unit == 'y':
            return  math.log(2)/(self.sf_half_life*365*24*3600) # s
        elif self.half_life_unit == 'd':
            return  math.log(2)/(self.sf_half_life*24*3600) # s
        elif self.half_life_unit == 's':
            return  math.log(2)/(self.sf_half_life) # s

    def get_decay_rate(self, mass, unit='g'):
        """
        The function calculates the decay rate for the nuclide.
        
        Parameters
        ----------
        mass : float
            the mass of the nuclide
        unit : str
            the unit for the mass with g as default. Alternatives are mg, kg.

        Returns
        -------
        float
            the decay rate for the nuclide
        """
        if unit=='g':
            N = mass/self.molar_mass*6.022E23
        elif unit=='kg':
            N = mass*1000/self.molar_mass*6.022E23
        if unit=='mg':
            N = mass*1E-3/self.molar_mass*6.022E23

        return self.get_lambda()*N
