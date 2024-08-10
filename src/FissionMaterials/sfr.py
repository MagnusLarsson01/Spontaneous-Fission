#from material import Material

class SpontaneousFissionResult():
    def __init__(self, spontaneous_fission_rate, unit):
        self.spontaneous_fission_rate = spontaneous_fission_rate
        self.unit = unit

    def __repr__(self):        
        return f"Sponteneous fission rate: {self.spontaneous_fission_rate} {self.unit}"


    