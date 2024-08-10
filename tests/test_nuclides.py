import unittest

from FissionMaterials.nuclide import *

class TestNuclides(unittest.TestCase):
    def setup(self):
        self.nuclides = dict()
        with open('../src/data/nuclides.csv') as file:
            first = True
            for row in file:
                if not first:
                    parts = row.split(',')        
                    half_life = math.inf if parts[5] == 'inf' else float(parts[5])
                    self.nuclide_data[parts[0]+parts[2]] = Nuclide(parts[0],parts[0]+parts[2],int(parts[1]),int(parts[2]),float(parts[3]),half_life)
                first = False

    def test_nuclide_notation(self):
        nuclide = Nuclide('U', 'U235', 92, 235, 235.044, 9.8E18)
        self.assertTrue(nuclide.get_nuclide_notation == '92235')

if __name__=="__main__":
    unittest.main()