

class Unit(object):
    def __init__(self, name, scaling):
        """
        Args:

            * name - String
            * scaling - String

        """
        self.name = name
        self.scaling = scaling

    def __str__(self):
        return 'UNIT["{n}",{s}]'.format(n=self.name, s=self.scaling)

    def wktcrs(self, ind=0):
        pattern = '{ind}UNIT["{n}",{s}]'
        result = pattern.format(ind=ind*'  ', n=self.name, s=self.scaling)
        return result


class AngleUnit(Unit):
    def __str__(self):
        return 'ANGLEUNIT["{n}",{s}]'.format(n=self.name, s=self.scaling)
    def wktcrs(self, ind=0):
        pattern = '{ind}ANGLEUNIT["{n}",{s}]'
        result = pattern.format(ind=ind*'  ', n=self.name, s=self.scaling)
        return result


class LengthUnit(Unit):
    def __str__(self):
        return 'LENGTHUNIT["{n}",{s}]'.format(n=self.name, s=self.scaling)
    def wktcrs(self, ind=0):
        pattern = '{ind}LENGTHUNIT["{n}",{s}]'
        result = pattern.format(ind=ind*'  ', n=self.name, s=self.scaling)
        return result



class Axis(object):
    """An Axis, the definition of meaning for a set of coordinate values."""

    axis = ('<axis keyword> <left delimiter>  <axis nameAbbrev> <wkt separator> '
            '<axis direction> [ <wkt separator> <axis order> ] [ <wkt separator> <axis unit> ] '
            '[ { <wkt separator> <identifier> } ]...  <right delimiter>')

    def __init__(self, name='', abbreviation='', direction='', unit=None):
        """
        Create an Axis.

        Kwargs:

            * name - a string.
            * abbreviation - a string.
            * direction - a string.
            * axis_unit - a :class:`terra.Unit`.

        """
        self.name = name
        self.abbreviation = abbreviation
        self.direction = direction
        self.unit = unit

    def nameabbv(self):
        if self.name and self.abbreviation:
            result = '{} ({})'.format(self.name, self.abbreviation)
        elif self.name:
            result = self.name
        elif self.abbreviation:
            result = '({})'.format(self.abbreviation)
        return result

    def __str__(self):
        # '       AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],\n'
        pattern = 'AXIS["{nameabbv}",{direction},{unit}]'
        result = pattern.format(nameabbv=self.nameabbv(), direction=self.direction,
                                unit=str(self.unit))
        return result

    def wktcrs(self, ind=0):
        pattern = '{ind}AXIS["{nameabbv}",{direction},{unit}]'
        result = pattern.format(ind=ind*'  ', nameabbv=self.nameabbv(), direction=self.direction,
                                unit=str(self.unit))
        return result


class CSystem(object):
    CSTYPES = set(('affine', 'Cartesian', 'cylindrical', 'ellipsoidal', 'linear',
                   'parametric', 'polar', 'spherical', 'temporal', 'vertical'))
    """A Coordinate System: a set of basis vectors defining an ordered collection of Axes."""
    def __init__(self, cstype='', dimension=None, identifier=None, axes=None):
        """
        Create a CSystem.

        Kwargs:

            * cstype
            * dimension - Integer: the number of degrees of freedom the basis is defined over.
            * identifier - String
            * axes - A list of :class:`Axis` instances.

        """
        self.identifier = identifier
        self.cstype = cstype
        self.dimension = dimension
        if axes is None:
            axes = []
        self.axes = axes

    @property
    def cstype(self):
        return self._cst

    @cstype.setter
    def cstype(self, cstype):
        if cstype not in self.CSTYPES:
            msg = '{} not in list of valid CSTypes:\n\t{}'.format(cstype, self.CSTYPES)
            raise ValueError(msg)
        self._cst = cstype

    @property
    def cs_unit(self):
        return self._csu

    @cs_unit.setter
    def cs_unit(self, cs_unit):
        if set([axis.unit for axis in axes]) != set(None):
           raise ValueError('CS unit cannot be set if contained axes have units')
        self._csu = cs_unit

    def wktcrs(self, ind=0):
        pattern = ('{ind}CS[{cstype},{dim}],\n'
                   '{ind}{axes}')
        axes_string = ',\n' + ind * '  '
        axes_string = axes_string.join([ax.wktcrs(ind+1) for ax in self.axes])
        result = pattern.format(ind=ind*'  ', cstype=self.cstype, dim=self.dimension,
                                axes=axes_string)
        return result


class Ellipsoid(object):
    """"""
    def __init__(self, name='', semi_major_axis=None, inverse_flattening=0, lunit=None):
        """Create an Ellipsoid""" 
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.inverse_flattening = inverse_flattening
        self.lunit = lunit

    def wktcrs(self, ind=0):
        pattern = ('{ind}ELLIPSOID["{name}",{sma},{ifl},\n'
                   '{ind}  {unit}]')
        result = pattern.format(ind=ind*'  ', name=self.name, sma=self.semi_major_axis,
                                ifl=self.inverse_flattening, unit=self.lunit.wktcrs(ind+1))
        return result


class Datum(object):
    """"""
    def __init__(self, name='', ellipsoid=None):
        """Create a Datum."""
        self.name = name
        self.ellipsoid = ellipsoid

    def wktcrs(self, ind=0):
        pattern = ('{ind}DATUM["{name}",\n'
                   '{ind}  {ellp}],\n')
        result = pattern.format(ind=ind*'  ', name=self.name, ellp=self.ellipsoid.wktcrs(1))
        return result


class GeodeticDatum(Datum):
    pass



class CRS(object):
    pass


# projected
## Cartesian 2
# vertical
## vertical 1
# engineering
## affine 2 or 3
## Cartesian 2 or 3
## cylindrical 3
## linear 1
## polar 2
## spherical 3
# image
## affine 2
## Cartesian 2
# parametric
## parametric 1
# temporal
## time 1 


class GeodeticCRS(CRS):
    """
    A geodetic coordinate reference system.
    """
    # Class attribute, as defined in ISO19162
    geodetic_crs= ('<geodetic crs keyword> <left delimiter> <crs name> '
                   '<wkt separator> <geodetic datum> <wkt separator> '
                   '<coordinate system> <scope extent identifier remark> '
                   '<right delimiter>')
    geodetic_crs_keyword = 'GEODCRS'
    geodetic_crs_keyword_set = set((geodetic_crs_keyword, 'GEODETICCRS'))
    CSTYPESDIMS = dict((('Cartesian', set((3,))),
                        ('ellipsoidal', set((2, 3))),
                        ('spherical', set((3,)))))

    def __init__(self, name='', datum=None, coord_system=None):
        """
        Kwargs:

            * name
            * datum
            * coord_system

        """
        self.crs_name = name
        self.datum = datum
        self.coord_system = coord_system

    @property
    def geodetic_datum(self):
        return self._gd
    @geodetic_datum.setter
    def geodetic_datum(self, gd):
        if not (isinstance(gd, GeodeticDatum) or None):
            raise TypeError('GeodeticDatum required, {} provided'.format(str(gd)))
        self._gd = gd

    @property
    def coord_system(self):
        return self._cs
    @coord_system.setter
    def coord_system(self, cs):
        if not (isinstance(cs, CSystem) or None):
            raise TypeError('CSystem required, {} provided'.format(str(gd)))
        self._cs = cs

    def wktcrs(self, ind=0):
        output = ('   GEODCRS["WGS 84",\n'
                  '     DATUM["World Geodetic System 1984",\n'
                  '       ELLIPSOID["WGS 84",6378137,298.257223563,\n'
                  '         LENGTHUNIT["metre",1.0]]],\n'
                  '     CS[ellipsoidal,3],\n'
                  '       AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '       AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],\n'
                  '       AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]]\n')
        pattern = ('{ind}{crs_kw}["{name}",\n'
                   '{ind}{datum}'
                   '{ind}{cs}]\n')
        result = pattern.format(ind=ind*'  ', crs_kw=self.geodetic_crs_keyword, name=self.crs_name,
                                datum=self.datum.wktcrs(ind), cs=self.coord_system.wktcrs(ind))
        return result


#     def __str__(self):
#         replacements = dict((('<geodetic crs keyword>', self.geodetic_crs_keyword),
#                              ('<crs name>', '"{}"'.format(self.crs_name))))
#         return wktformat(self.geodetic_crs, replacements)

# def wktformat(pattern_string, replacements):
#     updates = dict((('<left delimiter>', '['), ('<right delimiter>', ']'),
#                     ('<wkt separator>', ','), ('<scope extent identifier remark>', '')))
#     updates.update(replacements)
#     result = pattern_string
#     for key, value in updates.iteritems():
#         result = result.replace(key, value)
#     return result
