"""
The terra datetime module supplies classes for manipulating dates and times in
 both simple and complex ways. While date and time arithmetic is supported, the
 focus of the implementation is on efficient attribute extraction for output
 formatting and manipulation.

The interface is based on Python's :mod:`datetime.datetime`. This has effects,
 including the naming of classes without capitalisation where they support
 the Python :mod:`datetime.datetime` interface.

Different Calendars are supported, but numerical conversions between calendars
 is not supported, this is not a safe operation to generalise, case specific
 knowledge and logic is required.

"""


class date(object):
    """
    An idealized naive date,  Attributes: year, month, and day.

    Objects of this type are not immutable.

    """
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return '{0:0>4}-{1:0>2}-{2:0>2}'.format(self.year, self.month,
                                                self.day)

    def __repr__(self):
        return 'terra.datetime.date({}, {}, {})'.format(self.year,
                                                        self.month,
                                                        self.day)


class time(object):
    """
    An idealized instant in time, independent of any particular day.

    Attributes: hour, minute, second, microsecond, and tzinfo.

    Objects of this type are not immutable.

    """
    def __init__(self, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        """
        Create a time instance.

        Attrs:
            hour - int, default 0.
            minute - int, default 0.
            second - int, default 0.
            microsecond - int, default 0.
            tzinfo
        """
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.tzinfo = tzinfo

    def __str__(self):
        ms = ''
        if self.microsecond:
            ms = '.{0:0>6}'.format(self.microsecond)
        return '{0:0>2}:{1:0>2}:{2:0>2}{3}'.format(self.hour, self.minute,
                                                   self.second, ms)

    def __repr__(self):
        return 'terra.datetime.time({}, {}, {}, {})'.format(self.hour,
                                                            self.minute,
                                                            self.second, ms)


class datetime(object):
    """
    An idealized instant within a calendar, a combination of a
    :class:`terra.datetime.date` and a :class:`terra.datetime.time`.

    Attributes: year, month, day, hour, minute, second, microsecond,
    tzinfo and calendar.

    Objects of this type are not immutable.

    """
    def __init__(self, year, month, day, hour=0, minute=0, second=0,
                 microsecond=0, tzinfo=None, calendar=None):
        self.calendar = calendar
        # Design question: validate inputs?
        self.date = date(year, month, day)
        self.time = time(hour, minute, second, microsecond, tzinfo)


class timedelta(object):
    """
    A duration expressing the difference between two date, datetime instances
    to microsecond resolution.

    For date calculations, the calendars of the two datetime instances must
    match.

    Objects of this type are not immutable.

    """
    pass


class tzinfo(object):
    """
    An abstract base class for time zone information objects.
    These are used by the datetime and time classes to provide a customizable
    notion of time adjustment (for example, to account for time zone and/or
    daylight saving time).

    Objects of this type are not immutable.

    """
    pass


class Duration(object):
    """
    A datetime duration, represented by whole unit like quantities.

    For example 'April, 2012, ISO-Gregorian' is the whole month of April
    with respect to the ISO-Gregorian Calendar.

    """
    def __init__(self, year=None, month=None, day=None, hour=None,
                 calendar=None):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.calendar = calendar


class SegmentedDuration(object):
    """
    A datetime duration, represented by collections of unit like quantities.
    The duration may be segmented, for example: particular months within
    particular years.

    All defined elements match.
    

    """
    def __init__(self, year=None, month=None, day=None, hour=None,
                 calendar=None):
        self.years = year
        self.months = month
        self.days = day
        self.hours = hour
        self.calendar = calendar


class EpochDateTime(object):
    """
    An idealized instant within a calendar, a 'value and unit' numerical
    offset from a defined :class:`datetime` instance with respect to 
    a calendar.

    """
    def __init__(self, offset, unit, datetime):
        """
        Create an EpochDateTime instance.

        Args:

            * offsets - an int or float
            * unit - the temporal unit
            * datetime - a :class:`terra.datetime.datetime` instance

        """
        self.offset = offset
        self.unit = unit
        self.datetime = datetime

    @property
    def calendar(self):
        return self.datetime.calendar


class EpochDateTimeArray(object):
    """
    An idealized instant within a calendar, a 'value and unit' numerical
    offset from a defined :class:`datetime` instance with respect to 
    a calendar.

    """
    def __init__(self, offsets, unit, datetime):
        """
        Create an EpochDateTimeArray instance.

        Args:

            * offsets - a numpy array, masked array or array like object
            * unit - the temporal unit
            * datetime - a :class:`terra.datetime.datetime` instance

        """
        self.offsets = offsets
        self.unit = unit
        self.datetime = datetime

    @property
    def calendar(self):
        return self.datetime.calendar


class Calendar(object):
    """
    A representation of the relationship between the different elements of
    a potential datetime instance.

    This includes the definition of periodic and nested unit like quantities.

    """
    def __init__(self, url=None, days_in_year=None, days_in_leap_year=None,
                 leap_year_date=None, leap_year_years=None,
                 months_in_year=None, month_names=None,
                 month_day_map=None, leapsecond_datetimes=None,
                 days_in_week=None, weekday_names=None,
                 weekday_start_date=None):
        self.url = url
        self.days_in_year = days_in_year
        self.days_in_leap_year = days_in_leap_year
        self.leap_year_date = leap_year_date
        if leap_year_years is None:
            leap_year_years = []
        self.leap_year_years = leap_year_years
        self.months_in_year = months_in_year
        if month_names is None:
            month_names = []
        self.month_names = month_names
        self.month_day_map = month_day_map
        if leapsecond_datetimes is None:
            leapsecond_datetimes = []
        self.leapsecond_datetimes = leapsecond_datetimes
        self.days_in_week = days_in_week
        if weekday_names is None:
            weekday_names = []
        self.weekday_names = weekday_names
        self.weekday_start_date = weekday_start_date

