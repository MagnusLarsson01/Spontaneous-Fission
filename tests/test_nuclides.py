"""
tests for spontaneous fission package 

Magnus Larsson 2024
"""
import unittest
import math
from SpontaneousFission import *

class TestNuclides(unittest.TestCase):
    def setup(self):
        self.nuclides = dict()
        with open('../src/data/nuclides.csv') as file:
            first = True
            for row in file:
                if not first:
                    parts = row.split(',')        
                    half_life = math.inf if parts[5] == 'inf' else float(parts[5])
                    nuclide = Nuclide(parts[0],parts[0]+parts[2],int(parts[1]),int(parts[2]),float(parts[3]),half_life)
                    self.nuclide_data[parts[0]+parts[2]] = nuclide
                    self.nuclide_data[nuclide.get_nuclide_notation()] = nuclide
                first = False

    def test_nuclide_notation(self):
        nuclide = Nuclide('U', 'U235', 92, 235, 235.044, 9.8E18)
        self.assertTrue(nuclide.get_nuclide_notation() == '92235')

    def test_nuclide_lambda(self):
        nuclide = Nuclide('U', 'U235', 92, 235, 235.044, 9.8E18)
        self.assertTrue(nuclide.get_lambda()==2.2428115213968143e-27)

    def test_material_nuclide_load(self):
        material = Material()
        self.assertTrue(len(material.nuclide_data.keys())==54)

    def test_material_reference(self):
        uo2 = Material(amount_type='barn-1cm-1')
        uo2.add_nuclide('8016', 4.76318709979466E-02)
        uo2.add_nuclide('92232', 7.06104652673138E-15)
        uo2.add_nuclide('92233', 2.35088603140821E-11)
        uo2.add_nuclide('92234', 3.04159895434244E-08)
        uo2.add_nuclide('92235', 4.49538785711297E-04)
        uo2.add_nuclide('92236', 6.89750759080931E-05)
        uo2.add_nuclide('92238', 2.26704289203308E-02)
        uo2.add_nuclide('93237', 4.55266877773770E-06)
        uo2.add_nuclide('94236', 1.89748994915674E-14)
        uo2.add_nuclide('94238', 7.46428645473517E-07)
        uo2.add_nuclide('94239', 1.24397804220399E-04)
        uo2.add_nuclide('94240', 2.91722130669398E-05)
        uo2.add_nuclide('94241', 1.62079695976725E-05)
        uo2.add_nuclide('94242', 2.48409460618007E-06)
        uo2.add_nuclide('95241', 3.48993557415652E-07)
        uo2.add_nuclide('96242', 6.91986026960431E-08)
        uo2.add_nuclide('96244', 3.34182840687710E-08)
        uo2.add_nuclide('96246', 3.15376964764952E-11)
        uo2.set_volume('cm3', 1.0)
        sfr = uo2.getSFR()        
        self.assertTrue(str(sfr.density)[0:4]=='10.5')        
        self.assertTrue(sfr.volume==1.0)
        self.assertTrue(str(sfr.spontaneous_fission_rate)[0:5]=='292.9')        

if __name__=="__main__":
    unittest.main()