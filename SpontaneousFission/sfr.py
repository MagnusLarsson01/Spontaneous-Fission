"""
module for spontaneous fission result 

Magnus Larsson 2024
"""
class SpontaneousFissionResult():
    """
    A class used to represent a the result from spontaneous fission analysis of a material.
    An instance of the class can be printed to show a summary of the material including density, volume (if given), 
    atomic concentrations of nuclides and the total spontaneous fission rate.

    Parameters
    ----------
    concentrations : dict 
        Concentrations of the nuclides in the material
    density : float
        Density of the material
    volume : float
        Volume of the material
    spontaneous_fission_rate : float
        The total spontaneous fission rate of the material 
    unit : str
        The unit of the spontaneous fission rate (s-1, g-1s-1)
    error : boolean
        Indication if the spontaneous fission rate could not be calculated
    error_message : str
        The error message

    Attributes
    ----------
    concentrations : dict 
        Concentrations of the nuclides in the material
    density : float
        Density of the material
    volume : float
        Volume of the material
    spontaneous_fission_rate : float
        The total spontaneous fission rate of the material 
    unit : str
        The unit of the spontaneous fission rate (s-1, g-1s-1)
    error : boolean
        Indication if the spontaneous fission rate could not be calculated
    error_message : str
        The error message

    """
    def __init__(self, concentrations, density, volume, spontaneous_fission_rate, unit, error=False, error_message='', density_unit='barn^-1cm^-1'):
        self.spontaneous_fission_rate = spontaneous_fission_rate
        self.unit = unit
        self.error = error
        self.error_message = error_message
        self.concentrations = concentrations
        self.density = density
        self.volume = volume
        self.density_unit = density_unit

    def __repr__(self):
        if self.error:
            return f"Sponteneous fission rate failed: {self.error_message}"
        else:
            message = f"density={self.density}, volume={self.volume}\nList of nuclides, and atomic densities (in {self.density_units})\n"
            for nuclide, atomic_density in self.concentrations.items():
                message += f"{nuclide.get_nuclide_notation()}\t{atomic_density}\n"   
            message += f"\nSponteneous fission rate: {self.spontaneous_fission_rate} {self.unit}"
            return message
    