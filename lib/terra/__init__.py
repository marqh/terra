import copy
import re
import six

import terra.cartopy_import_manager as ccrs

import terra.units
from terra.units import BaseUnit
import terra.datetime

__version__ = '0.3'


class Axis(object):
    """An Axis, the definition of meaning for a set of coordinate values."""

    axis = ('<axis keyword> <left delimiter>  <axis nameAbbrev> '
            '<wkt separator> <axis direction> [ <wkt separator> <axis order> ]'
            ' [ <wkt separator> <axis unit> ] '
            '[ { <wkt separator> <identifier> } ]...  <right delimiter>')

    def __init__(self, name='', abbreviation='', direction='', unit=None):
        """
        Create an Axis.

        Kwargs:

            * name - a string.
            * abbreviation - a string.
            * direction - a string.
            * axis_unit - a :class:`terra.units.Unit`.

        """
        self.name = name.strip()
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
        pattern = 'AXIS["{nameabbv}",{direction},{unit}]'
        result = pattern.format(nameabbv=self.nameabbv(),
                                direction=self.direction,
                                unit=str(self.unit))
        return result

    def __repr__(self):
        return self.__str__()

    def wktcrs(self, ind=0):
        pattern = '{ind}AXIS["{nameabbv}",{direction},{unit}]'
        result = pattern.format(ind=ind*'  ', nameabbv=self.nameabbv(),
                                direction=self.direction,
                                unit=self.unit.wktcrs())
        return result

    _wkt_pattern = ('\s*AXIS\[(?P<nameabbv>"[\w\s\(\)]+")\s*,(?P<dir>\w+)\s*,'
                    '\s*(?P<unit>{unit}\[.+\])\s*\]\s*')
    lu = terra.units.LengthUnit.ustring
    au = terra.units.AngleUnit.ustring
    wkt_patterns = [re.compile(_wkt_pattern.format(unit=lu)),
                    re.compile(_wkt_pattern.format(unit=au)),
                    re.compile('\s*AXIS\[(?P<nameabbv>"[\w\s\(\)]+")\s*,'
                               '(?P<dir>\w+)\s*\]\s*')]

    name_abbv_pattern = re.compile('"([\s\w]*)\(?(\w*)\)?"')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        matches = [wkt_pattern.match(wktcrs_string) for
                   wkt_pattern in cls.wkt_patterns]
        ax = None
        for match in matches:
            if match:
                na_match = cls.name_abbv_pattern.match(match.group('nameabbv'))
                name = na_match.groups()[0]
                abbv = na_match.groups()[1]
                # yuck
                try:
                    unit = BaseUnit.parse_wktcrs(match.group('unit'),
                                                 strict=strict)
                except IndexError:
                    unit = None
                ax = cls(name=name, abbreviation=abbv,
                         direction=match.group('dir'), unit=unit)
        return ax


class CSystem(object):
    """
    A Coordinate System: a set of basis vectors defining an ordered collection
    of Axes.

    """
    CSTYPES = set(('affine', 'Cartesian', 'cylindrical', 'ellipsoidal',
                   'linear', 'parametric', 'polar', 'spherical', 'temporal',
                   'vertical'))

    def __init__(self, cstype='', dimension=None, identifier=None, axes=None,
                 cs_unit=None):
        """
        Create a CSystem.

        Kwargs:

            * cstype
            * dimension - Integer: the number of degrees of freedom the basis
                                   is defined over.
            * identifier - String
            * axes - A list of :class:`Axis` instances.

        """
        self.identifier = identifier
        self.cstype = cstype
        self.dimension = dimension
        if axes is None:
            axes = []
        self.axes = axes
        if cs_unit is not None:
            self.cs_unit = cs_unit

    def __str__(self):
        return '{} {}, ({}) {}'.format(self.identifier, self.cstype,
                                       self.dimension, self.axes)

    def __repr__(self):
        return self.__str__()

    @property
    def cstype(self):
        return self._cst

    @cstype.setter
    def cstype(self, cstype):
        if cstype not in self.CSTYPES:
            msg = '{} not in list of valid CSTypes:\n\t{}'.format(cstype,
                                                                  self.CSTYPES)
            raise ValueError(msg)
        self._cst = cstype

    @property
    def cs_unit(self):
        return self._csu

    @cs_unit.setter
    def cs_unit(self, cs_unit):
        if set([axis.unit for axis in self.axes]) != set((None,)):
            raise ValueError('CS unit cannot be set if contained axes '
                             'have units defined.')
        self._csu = cs_unit

    def wktcrs(self, ind=0):
        pattern = ('{ind}CS[{cstype},{dim}],\n'
                   '{ind}{axes}')
        axes_string = ',\n' + ind * '  '
        axes_string = axes_string.join([ax.wktcrs(ind+1) for ax in self.axes])
        result = pattern.format(ind=ind*'  ', cstype=self.cstype,
                                dim=self.dimension, axes=axes_string)
        return result

    def validate(self, exceptions=None):
        if exceptions is None:
            exceptions = []
        if self.dimension != len(self.axes):
            msg = ('The list of axes:\n{} must be the same length as the '
                   'dimension value '
                   'of the CSystem: {}'.format(self.axes, self.dimension))
            exceptions.append(ValueError(msg))
        return exceptions

    wkt_pattern = re.compile('CS\[(?P<cstype>\w+)\s*,\s*(?P<dim>[0-9\.]+)\],'
                             '(?P<axes>.+)')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)
        cs = None
        if match:
            ax_list = re.findall('\s*(AXIS\[.+?\]\]),?\s*',
                                 match.group('axes'))
            if ax_list:
                axes = [Axis.parse_wktcrs(ax) for ax in ax_list]
                cs = cls(match.group('cstype'), match.group('dim'),
                         identifier='', axes=axes)
            else:
                ax_list = re.findall('\s*(AXIS\[.+?\]),?\s*',
                                     match.group('axes'))
                axes = [Axis.parse_wktcrs(ax) for ax in ax_list]
                unitstr = re.match('.*,([A-Z]+UNIT\[.*\])',
                                   match.group('axes'))
                unit = terra.units.BaseUnit.parse_wktcrs(unitstr.groups()[0],
                                                         strict=strict)
                cs = cls(match.group('cstype'), match.group('dim'),
                         identifier='', axes=axes, cs_unit=unit)
        return cs


class Ellipsoid(ccrs.Globe):
    """"""
    def __init__(self, name='', semimajor_axis=None, inverse_flattening=0,
                 lunit=None):
        """
        Create an Ellipsoid

        Kwargs:

            * name - String.
            * semimajor_axis - String or Float, a string will be preserved.
            * inverse_flattening - String or Float, a string will be preserved.
            * lunit - :class:`terra.units.LenthUnit` instance.

        """
        self.name = name
        self.semimajor_axis = semimajor_axis
        self.inverse_flattening = inverse_flattening
        self.lunit = lunit

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.name, self.semimajor_axis,
                                       self.inverse_flattening, self.lunit)

    def __repr__(self):
        return self.__str__()

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
        result = pattern.format(ind=ind*'  ', name=self.name,
                                sma=self.semimajor_axis_string,
                                ifl=self.inverse_flattening_string,
                                unit=self.lunit.wktcrs(ind+1))
        return result

    wkt_pattern = re.compile('\s*ELLIPSOID\["(?P<name>[a-zA-Z0-9\s]+)"\s*,'
                             '\s*(?P<smax>[0-9\.]+)\s*,'
                             '\s*(?P<invf>[0-9\.]+)\s*,'
                             '\s*(?P<lunit>LENGTHUNIT\[.+\])\]\s*')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)  # , strict=strict)
        ellipsoid = None
        if match:
            lunit = terra.units.BaseUnit.parse_wktcrs(match.group('lunit'))
            ellipsoid = Ellipsoid(name=match.group('name'),
                                  semimajor_axis=match.group('smax'),
                                  inverse_flattening=match.group('invf'),
                                  lunit=lunit)
        return ellipsoid


class GeodeticDatum(ccrs.Geodetic):
    """"""

    def __init__(self, name='', ellipsoid=None):
        """Create a Datum."""
        self.name = name
        self.ellipsoid = ellipsoid

    @property
    def globe(self):
        """
        Return a copy of the ellipsoid with the proj4 datum defined from
        the :class:`Datum` name.

        """
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
        ellp = None
        if self.ellipsoid is not None:
            ellp = self.ellipsoid.wktcrs(1)
        result = pattern.format(ind=ind*'  ', name=self.name, ellp=ellp)
        return result

    wkt_pattern = re.compile('DATUM\["(?P<name>[a-zA-Z0-9 ]+)",'
                             '(?P<ellps>.+)\]')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)  # , strict=strict)
        gd = None
        if match:
            ellipsoid = Ellipsoid.parse_wktcrs(match.group('ellps'), strict)
            gd = GeodeticDatum(name=match.group('name'), ellipsoid=ellipsoid)
        return gd


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
        if not isinstance(result, ccrs.CRS):
            raise TypeError('This CRS cannot return a cartopy CRS.')
        return result

    def validate(self, exceptions=None):
        if exceptions is None:
            exceptions = []
        if self.coord_system is not None:
            if self.coord_system.name not in self.allowed_cs_names:
                msg = ('The coord system must be one of the allowed names')
                exceptions.append(ValueError(msg))
            if (self.coord_system.dimension not in
               self.allowed_dimension_size.get(self.coord_system.name)):
                msg = ('The coord system dimension size must be allowed for '
                       'the coord system name.')
                exceptions.append(ValueError(msg))
            exceptions = exceptions + self.coord_system.validate()
        return exceptions

    def wktcrs(self, ind=0):
        pattern = ('{ind}{crs_kw}["{name}",\n'
                   '{ind}{datum}'
                   '{ind}{cs}]\n')
        result = pattern.format(ind=ind*'  ', crs_kw=self.geodetic_crs_keyword,
                                name=self.crs_name,
                                datum=self.datum.wktcrs(ind),
                                cs=self.coord_system.wktcrs(ind))
        return result


class GeodeticCRS(CRS):
    """
    A geodetic coordinate reference system.

    """
    # Class attribute, as defined in ISO19162
    geodetic_crs = ('<geodetic crs keyword> <left delimiter> <crs name> '
                    '<wkt separator> <geodetic datum> <wkt separator> '
                    '<coordinate system> <scope extent identifier remark> '
                    '<right delimiter>')
    geodetic_crs_keyword = 'GEODCRS'
    geodetic_crs_keyword_set = set((geodetic_crs_keyword, 'GEODETICCRS'))
    CSTYPESDIMS = dict((('Cartesian', set((3,))),
                        ('ellipsoidal', set((2, 3))),
                        ('spherical', set((3,)))))
    wkt_pattern = re.compile('^\s*([a-zA-Z0-9 ]+)\['
                             '"([a-zA-Z0-9 ]+)",\s*'
                             '(DATUM\[.+\]),\s*'
                             '(CS\[.+\])\]')

    @property
    def geodetic_datum(self):
        return self.datum

    @geodetic_datum.setter
    def geodetic_datum(self, gd):
        if not (isinstance(gd, GeodeticDatum) or None):
            raise TypeError('GeodeticDatum required, {} '
                            'provided'.format(str(gd)))
        self.datum = gd

    def allowed_coord_names(self):
        return self.allowed_dimension_size.keys()

    def allowed_dimension_size(self):
        return {'Cartesian': set(3,),
                'ellipsoidal': set(2, 3),
                'spherical': set(3)}

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)
        if match:
            crstype, name, datum, coord_system = match.groups()
        datum = GeodeticDatum.parse_wktcrs(datum)
        coord_system = CSystem.parse_wktcrs(coord_system)
        crs = GeodeticCRS(name, datum, coord_system)
        return crs


class TemporalCRS(CRS):
    """
    A temporal coordinate reference system.

    """
    # Class attribute, as defined in ISO19162
    geodetic_crs = ('<temporal crs keyword> <left delimiter> <crs name> '
                    '<wkt separator> <temporal datum> <wkt separator> '
                    '<coordinate system> <scope extent identifier remark> '
                    '<right delimiter>')
    temporal_crs_keyword = 'TIMECRS'
    temporal_crs_keyword_set = set((temporal_crs_keyword,))
    CSTYPESDIMS = {'time': set((1,))}
    wkt_pattern = re.compile('^\s*([a-zA-Z0-9 ]+)\['
                             '"([a-zA-Z0-9 ]+)",\s*'
                             '(TDATUM\[.+\]),\s*'
                             '(CS\[.+\])\]')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)
        if match:
            crstype, name, datum, coord_system = match.groups()
        datum = TemporalDatum.parse_wktcrs(datum)
        coord_system = CSystem.parse_wktcrs(coord_system)
        crs = TemporalCRS(name, datum, coord_system)
        return crs

    def as_cartopy_crs(self):
        raise TypeError('A TemporalCRS cannot return a cartopy CRS.')

    def epoch_datetimes(self, time_values):
        """"""
        calendar = terra.datetime.ISOGregorian()
        epoch = terra.datetime.datetime(year, month, day,
                                        hour, minute, second,
                                        microsecond, calendar=calendar)
        edt = terra.datetime.EpochDateTimes(time_values, tunit, epoch)

    def datetime_strings(self, coord_values):
        u = self.coord_system.cs_unit.unit
        edt = terra.datetime.EpochDateTimes(coord_values, u,
                                            self.datum.timeorigin)
        return str(edt)


class TemporalDatum(object):
    """"""

    def __init__(self, timeorigin, name='Time origin'):
        """Create a Datum."""
        if isinstance(timeorigin, terra.datetime.datetime):
            self.timeorigin = timeorigin
        else:
            pattern = re.compile('([0-9]+)-([0-9]+)-([0-9]+)'
                                 'T([0-9]+):([0-9]+):([0-9]+)\.?([0-9]+)Z')
            mch = pattern.match(timeorigin)
            if mch:
                isg = terra.datetime.ISOGregorian()
                self.timeorigin = terra.datetime.datetime(int(mch.group(1)),
                                                          int(mch.group(2)),
                                                          int(mch.group(3)),
                                                          int(mch.group(4)),
                                                          int(mch.group(5)),
                                                          int(mch.group(6)),
                                                          int(mch.group(7)),
                                                          calendar=isg)
        self.name = name

    def wktcrs(self, ind=0):
        pattern = ('{ind}DATUM["{name}",{timo}],\n')

        result = pattern.format(ind=ind*'  ', name=self.name,
                                timo=self.timeorigin)
        return result

    wkt_pattern = re.compile('TDATUM\["(?P<name>[a-zA-Z0-9 ]+)",'
                             'TIMEORIGIN\[(?P<tstamp>.+)\]\]')

    @classmethod
    def parse_wktcrs(cls, wktcrs_string, strict=False):
        match = cls.wkt_pattern.match(wktcrs_string)  # , strict=strict)
        gd = None
        if match:
            timeorigin = match.group('tstamp')
            gd = TemporalDatum(name=match.group('name'), timeorigin=timeorigin)
        return gd


def parse_wktcrs(wktcrs_string, strict=False):
    """
    Returns a Terra Coordinate Reference System, if one can be idenitifed, from
    a provided plain text string conforming to ISO19162.
    If the identity of the Terra type is inconclusive or unable to be defined,
    None is returned.

    Args:

        * wktcrs_string - the string to be parsed.

    Kwargs:

        * strict - Boolean: set to True to raise exceptions in cases of failed
                            parsing and failure to validate objects.

    """
    exceptions = []
    # Ignore newline characters
    wktcrs = wktcrs_string.replace('\n', '')
    pattern = re.compile('^\s*([a-zA-Z0-9 ]+)\[(.+)\]\s*')
    match = pattern.match(wktcrs)
    if match:
        crstype, crsdef = match.groups()
    else:
        exceptions.append('Pattern: (crs name)[(crs definition)] not matched')
    if crstype in GeodeticCRS.geodetic_crs_keyword_set:
        crs = GeodeticCRS.parse_wktcrs(wktcrs)
    elif crstype in TemporalCRS.temporal_crs_keyword_set:
        crs = TemporalCRS.parse_wktcrs(wktcrs)
    else:
        raise TypeError('Failed to parse wktcrs string'
                        ':{}'.format(wktcrs_string))
    if strict and exceptions:
        raise ValueError('\n'.join(exceptions))
    return crs
