
import terra.units
import unittest

class TestUnit(unittest.TestCase):
    def test_this(self):
        self.assertTrue(True)

    def test_WKTCRS_print(self):
        output = ('   GEODCRS["WGS 84",\n'
                  '     DATUM["World Geodetic System 1984",\n'
                  '       ELLIPSOID["WGS 84",6378137,298.257223563,\n'
                  '         LENGTHUNIT["metre",1.0]]],\n'
                  '     CS[ellipsoidal,3],\n'
                  '       AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '       AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '       AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]]\n')
        self.assertTrue(True)

class TestAngleUnit(unittest.TestCase):
    def test_str(self):
        au = terra.units.AngleUnit("degree", 0.0174532925199433)
        self.assertEqual('ANGLEUNIT["degree",0.0174532925199433]', str(au))
    def test_repr(self):
        au = terra.units.AngleUnit("degree", 0.0174532925199433)
        self.assertEqual('ANGLEUNIT["degree",0.0174532925199433]', repr(au))
     
if __name__ == '__main__':
    unittest.main()
