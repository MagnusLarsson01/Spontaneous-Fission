"""
module for spontaneous fission material 

Magnus Larsson 2024
"""
import importlib.resources
import math

class Material():
    """
    A class used to represent a material.
    List of default nuclides: Th232, U232, U233, U234, U235, U236, U238, Np237, 
    Pu236, Pu238, Pu239, Pu240, Pu241, Pu242, Am241, Cm242, Cm244, Cm246, Cm248, 
    Bk249, Cf246, Cf250, Cf252, Cf254, Fm257, No252.

    Parameters
    ----------
    amount_type : str
        Type of amount to be used for the material. Default is 'fraction' for number fractions with 'barn-1cm-1' as an alternative.  

    Attributes
    ----------
    amount_type : str
        Type of amount to be used for the material. Default is 'fraction' for number fractions with 'barn-1cm-1' as an alternative.  
    density : float 
        Density of the material.
    nuclide_data : dict
        The nuclide data loaded from resource file. Contains data for the default nuclides.
    material_data : dict
        The nuclides added to the material and the amount.
    volume : float
        The volume of the material.
    total_fraction_times_A : float 
        Totl fractions multiplies by mass number. Used for normalization of the fractions.    
        
    """
    def __init__(self, amount_type='fraction'):
        self.density = None
        self.nuclide_data = dict()
        self.load_nuclide_data()
        self.material_data = dict()
        self.volume = None
        self.total_fraction_times_A = 0.0
        self.amount_type = amount_type

    def load_nuclide_data(self):
        from SpontaneousFission import Nuclide 
        with importlib.resources.open_text('SpontaneousFission.data', 'nuclides.csv') as file:
            first = True
            for row in file:
                if not first:
                    parts = row.split(',')        
                    half_life = math.inf if parts[5] == 'inf' else float(parts[5])
                    nuclide = Nuclide(parts[0],parts[0]+parts[2],int(parts[1]),int(parts[2]),float(parts[3]),half_life)
                    self.nuclide_data[parts[0]+parts[2]] = nuclide
                    self.nuclide_data[nuclide.get_nuclide_notation()] = nuclide
                first = False

    def add_nuclide(self, name, amount):        
        nuclide = self.nuclide_data[name]        
        if self.amount_type=='fraction':
            self.material_data[nuclide] = amount
            self.total_fraction_times_A += amount*nuclide.A # weight fraction (non-normalized)
        elif self.amount_type=='barn-1cm-1':
            self.material_data[nuclide] = amount #*1E24*nuclide.molar_mass/6.022E23 # g per cm3

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
            if self.amount_type == 'fraction':
                fission_rates.append(nuclide.get_decay_rate(1)*fraction*nuclide.A)
            else:            
                fission_rates.append(nuclide.get_decay_rate(1)*fraction*1E24*nuclide.molar_mass/6.022E23)

        if self.amount_type == 'fraction':
            fission_rate = sum([x/self.total_fraction_times_A for x in fission_rates])
        else:
            fission_rate = sum(fission_rates)

        # print(fission_rate*self.density*self.volume)
        if self.volume is None:
            return fission_rate, 'fission/g/second'
        else:
            if self.amount_type == 'fraction':
                return fission_rate*self.density*self.volume, 'fission/second'
            else:
                return fission_rate*self.volume, 'fission/second'

    def calculate_nuclide_concentrations(self):
        conc = dict()
        for nuclide, fraction in self.material_data.items():
            if self.amount_type == 'fraction':
                if self.volume is None:                    
                    conc[nuclide] = (fraction*nuclide.A/self.total_fraction_times_A)*self.density*6.022E23/(nuclide.molar_mass*1E24)
                else:
                    conc[nuclide] = (fraction*nuclide.A/self.total_fraction_times_A)*self.density*self.volume*6.022E23/(nuclide.molar_mass*1E24)
            else:
                conc[nuclide] = fraction
        return conc
    
    def setDensity(self):
        self.density = 0.0
        for nuclide, amount in self.material_data.items():
            self.density += amount*1E24*nuclide.molar_mass/6.022E23

    def getSFR(self):
        from SpontaneousFission import SpontaneousFissionResult
        if self.density is None: 
            if self.amount_type=='fraction':
                return SpontaneousFissionResult(None, None, None, None, 'fission/second', error=True, error_message='No density was provided!')
            else:
                self.setDensity()
        fission_rate, unit = self.calculate_fission_rate()
        nuclide_concentrations = self.calculate_nuclide_concentrations()
        if self.volume is None:
            sfr = SpontaneousFissionResult(nuclide_concentrations, self.density, self.volume, fission_rate, unit, density_unit='barn-1cm-1cm-3')
        else:
            sfr = SpontaneousFissionResult(nuclide_concentrations, self.density, self.volume, fission_rate, unit)           
        return sfr

    def __repr__(self):
        return "Todo"
    
if __name__=="__main__":
    # 1g of U235 should be 0.00563 fissions per Kg per second
    uo2 = Material()
    uo2.add_nuclide('U235', 0.04)
    uo2.add_nuclide('U238', 0.96)
    uo2.add_nuclide('O16', 2.0)
    uo2.set_density('g/cm3', 10.5)
    # uo2.set_volume('cm3', 100)

    # 1g of U235 should be 0.00563 fissions per Kg per second
    # uo2 = Material()
    # uo2.add_nuclide('U238', 1.0)
    # # uo2.add_nuclide('U235', 1.0)
    # uo2.set_density('g/cm3', 18.95)
    # uo2.set_volume('cm3', 0.0528)

    # 1kg of Pu239 should be 0.00563 fissions per Kg per second
    # uo2 = Material()
    # uo2.add_nuclide('Pu238', 1.0)
    # uo2.set_density('g/cm3', 19.86)
    # uo2.set_volume('cm3', 0.05035)

    # 1kg of Pu239 should be 0.00563 fissions per Kg per second
    # uo2 = Material(amount_type='barn-1cm-1')
    # uo2.add_nuclide('Pu238', 0.0025296073169809577)
    # uo2.set_volume('cm3', 1.0)

    # 1kg of Pu239 should be 0.00563 fissions per Kg per second
    # uo2 = Material(amount_type='barn-1cm-1')
    # uo2.add_nuclide('8016', 4.76318709979466E-02)
    # uo2.add_nuclide('92232', 7.06104652673138E-15)
    # uo2.add_nuclide('92233', 2.35088603140821E-11)
    # uo2.add_nuclide('92234', 3.04159895434244E-08)
    # uo2.add_nuclide('92235', 4.49538785711297E-04)
    # uo2.add_nuclide('92236', 6.89750759080931E-05)
    # uo2.add_nuclide('92238', 2.26704289203308E-02)
    # uo2.add_nuclide('93237', 4.55266877773770E-06)
    # uo2.add_nuclide('94236', 1.89748994915674E-14)
    # uo2.add_nuclide('94238', 7.46428645473517E-07)
    # uo2.add_nuclide('94239', 1.24397804220399E-04)
    # uo2.add_nuclide('94240', 2.91722130669398E-05)
    # uo2.add_nuclide('94241', 1.62079695976725E-05)
    # uo2.add_nuclide('94242', 2.48409460618007E-06)
    # uo2.add_nuclide('95241', 3.48993557415652E-07)
    # uo2.add_nuclide('96242', 6.91986026960431E-08)
    # uo2.add_nuclide('96244', 3.34182840687710E-08)
    # uo2.add_nuclide('96246', 3.15376964764952E-11)
    # uo2.set_volume('cm3', 1.0)

    sfr = uo2.getSFR()
    print(sfr)
