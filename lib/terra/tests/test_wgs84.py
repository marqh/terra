
import terra
import unittest
class TestWGS84(unittest.TestCase):
    def setUp(self):
        self.wktoutput = ('  GEODCRS["WGS 84",\n'
                       '    DATUM["World Geodetic System 1984",\n'
                       '      ELLIPSOID["WGS 84",6378137,298.257223563,\n'
                       '        LENGTHUNIT["metre",1.0]]],\n'
                       '    CS[ellipsoidal,3],\n'
                       '      AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],\n'
                       '      AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],\n'
                       '      AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]]\n')
        self.wktinput = ('GEODCRS["WGS 84",'
                         'DATUM["World Geodetic System 1984",'
                         'ELLIPSOID["WGS 84",6378137,298.257223563,'
                         'LENGTHUNIT["metre",1.0]]],'
                         'CS[ellipsoidal,3],'
                         'AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],'
                         'AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],'
                         'AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]]')
        
    def test_this(self):
        self.assertTrue(True)

    def test_WKTCRS_print(self):
        du = terra.AngleUnit("degree", '0.0174532925199433')
        mu = terra.LengthUnit("metre", '1.0')
        axes = [terra.Axis(abbreviation='lat', direction='north', unit=du),
                terra.Axis(abbreviation='lon', direction='east', unit=du),
                terra.Axis(name='ellipsoidal height', abbreviation='h', direction='up', unit=mu),]
        cs = terra.CSystem(cstype='ellipsoidal', dimension=3, axes=axes)
        ep = terra.Ellipsoid(name="WGS 84", semimajor_axis='6378137',
                             inverse_flattening='298.257223563', lunit=mu)
        gd = terra.GeodeticDatum(name="World Geodetic System 1984", ellipsoid=ep)
        geodcrs = terra.GeodeticCRS(name="WGS 84", datum=gd, coord_system=cs)
        # print(geodcrs.wktcrs(1))
        # print(self.wktoutput)
        # print(geodcrs.wktcrs_strict())
        self.assertEqual(geodcrs.wktcrs(1), self.wktoutput)

    def test_parse_wkt(self):
        wgs84 = terra.parse_wktcrs(self.wktoutput, strict=True)
        self.assertEqual(wgs84.wktcrs(1), self.wktoutput)

    def test_parse_wkt_strict(self):
        wgs84 = terra.parse_wktcrs(self.wktinput, strict=True)
        self.assertEqual(wgs84.wktcrs_strict(), self.wktinput)
        
     
if __name__ == '__main__':
    unittest.main()
