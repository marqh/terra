
import terra
import unittest
class TestWGS84(unittest.TestCase):
    def test_this(self):
        self.assertTrue(True)

    def test_WKTCRS_print(self):
        du = terra.AngleUnit("degree", '0.0174532925199433')
        mu = terra.LengthUnit("metre", '1.0')
        axes = [terra.Axis(abbreviation='lat', direction='north', unit=du),
                terra.Axis(abbreviation='lon', direction='east', unit=du),
                terra.Axis(name='ellipsoidal height', abbreviation='h', direction='up', unit=mu),]
        cs = terra.CSystem(cstype='ellipsoidal', dimension=3, axes=axes)
        ep = terra.Ellipsoid(name="WGS 84", semi_major_axis='6378137',
                             inverse_flattening='298.257223563', lunit=mu)
        gd = terra.GeodeticDatum(name="World Geodetic System 1984", ellipsoid=ep)
        geodcrs = terra.GeodeticCRS(name="WGS 84", datum=gd, coord_system=cs)
        output = ('  GEODCRS["WGS 84",\n'
                  '    DATUM["World Geodetic System 1984",\n'
                  '      ELLIPSOID["WGS 84",6378137,298.257223563,\n'
                  '        LENGTHUNIT["metre",1.0]]],\n'
                  '    CS[ellipsoidal,3],\n'
                  '      AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '      AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '      AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]]\n')
        self.assertEqual(geodcrs.wktcrs(1), output)
        
     
if __name__ == '__main__':
    unittest.main()
