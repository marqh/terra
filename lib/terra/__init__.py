import copy

import cartopy

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

    def validate(self, exceptions=None):
        if exceptions is None:
            exceptions = []
        if self.dimension != len(self.axes):
            msg = ('The list of axes:\n{} must be the same length as the dimension value '
                   'of the CSystem: {}'.format(self.axes, self.dimension))
            exceptions.append(ValueError(msg))
        return exceptions

class Ellipsoid(cartopy.crs.Globe):
    """"""
    def __init__(self, name='', semimajor_axis=None, inverse_flattening=0, lunit=None):
        """
        Create an Ellipsoid
        
        Kwargs:

            * name - String.
            * semimajor_axis - String or Int, a string will be preserved.
            * inverse_flattening - String or Int, a string will be preserved.
            * lunit - :class:`Unit` instance.

        """ 
        self.name = name
        self.semimajor_axis = semimajor_axis
        self.inverse_flattening = inverse_flattening
        self.lunit = lunit

    @property
    def semimajor_axis(self):
        return float(self._semimajor_axis)

    @semimajor_axis.setter
    def semimajor_axis(self, smi):
        self._semimajor_axis = smi

    @property
    def semimajor_axis_string(self):
        return str(self._semimajor_axis)

    @property
    def inverse_flattening(self):
        return float(self._inverse_flattening)

    @inverse_flattening.setter
    def inverse_flattening(self, smi):
        self._inverse_flattening = smi

    @property
    def inverse_flattening_string(self):
        return str(self._inverse_flattening)

    @property
    def ellipse(self):
        return self.wkt2proj.get(self.name)

    @property
    def wkt2proj(self):
        return {'WGS 84': 'WGS84'}

    @property
    def flattening(self):
        if self.inverse_flattening == 0:
            result = 0
        else:
            result = 1 / self.inverse_flattening
        return result
    

    def wktcrs(self, ind=0):
        pattern = ('{ind}ELLIPSOID["{name}",{sma},{ifl},\n'
                   '{ind}  {unit}]')
        result = pattern.format(ind=ind*'  ', name=self.name, sma=self.semimajor_axis_string,
                                ifl=self.inverse_flattening_string, unit=self.lunit.wktcrs(ind+1))
        return result


class GeodeticDatum(cartopy.crs.Geodetic):
    """"""
    def __init__(self, name='', ellipsoid=None):
        """Create a Datum."""
        self.name = name
        self.ellipsoid = ellipsoid

    @property
    def globe(self):
        """Return a copy of the ellipsoid with the proj4 datum defined from the :class:`Datum` name."""
        ellipsoid = copy.copy(self.ellipsoid)
        if ellipsoid is not None:
            ellipsoid.datum = self.wkt2proj.get(self.name)
        return ellipsoid

    @property
    def wkt2proj(self):
        return {'World Geodetic System 1984': 'WGS84'}


    def wktcrs(self, ind=0):
        pattern = ('{ind}DATUM["{name}",\n'
                   '{ind}  {ellp}],\n')
        result = pattern.format(ind=ind*'  ', name=self.name, ellp=self.ellipsoid.wktcrs(1))
        return result




# geodetic
## Cartesian 3
## ellipsoidal 2 or 3
## spherical 	3
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


class CRS(object):
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

    def wktcrs_strict(self):
        """
        Return the strict Well Known Text Coordinate Reference System string,
        with no extraneous white space.

        """
        result = ''
        for line in self.wktcrs().split('\n'):
            result = result + line.lstrip()
        return result

    def as_cartopy_crs(self):
        result = self.datum
        if not isinstance(result, cartopy.CRS):
            raise TypeError('This CRS cannot return a cartopy CRS.')
        return result

    def validate(self, exceptions=None):
        if exceptions is None:
            exceptions = []
        if self.coord_system is not None:
            if self.coord_system.name not in self.allowed_cs_names:
                msg = ('The coord system must be one of the allowed names')
                exceptions.append(ValueError(msg))
            if self.coord_system.dimension not in self.allowed_dimension_size.get(self.coord_system.name):
                msg = ('The coord system dimension size must be allowed for the coord system name.')
                exceptions.append(ValueError(msg))
            exceptions = exceptions + self.coord_system.validate()
        return exceptions


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


    @property
    def geodetic_datum(self):
        return self.datum
    @geodetic_datum.setter
    def geodetic_datum(self, gd):
        if not (isinstance(gd, GeodeticDatum) or None):
            raise TypeError('GeodeticDatum required, {} provided'.format(str(gd)))
        self.datum = gd

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

    def allowed_coord_names(self):
        return self.allowed_dimension_size.keys()

    def allowed_dimension_size(self):
        return {'Cartesian': set(3,),
                'ellipsoidal': set(2, 3),
                'spherical': set(3)}
