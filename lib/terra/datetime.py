"""
The terra datetime module supplies classes for manipulating dates and times in both simple and complex ways. While date and time arithmetic is supported, the focus of the implementation is on efficient attribute extraction for output formatting and manipulation.

The interface is based on Python's :mod:`datetime.datetime`. This has effects, inlcuding the naming of classes without capitalisation where they support the Python :mod:`datetime.datetime` interface.

Different Calendars are supported, but numerical conversions between calendars is not supported, this is not a safe operation to generalise, case specific knowledge and logic is required.

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
        return '{0:0>4}-{1:0>2}-{2:0>2}'.format(self.year, self.month, self.day)

    def __repr__(self):
        return 'terra.datetime.date({}, {}, {}, {})'.format(self.year, self.month, self.day)
        


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
        return '{0:0>2}:{1:0>2}:{2:0>2}{3}'.format(self.hour, self.minute, self.second, ms)

    def __repr__(self):
        return 'terra.datetime.time({}, {}, {}, {})'.format(self.hour, self.minute,
                                                            self.second, ms)

class datetime(object):
    """
    A idealized instant within a calendar, a combination of a :class:`terra.datetime.date`
    and a :class:`terra.datetime.time`.

    Attributes: year, month, day, hour, minute, second, microsecond, tzinfo and calendar.

    Objects of this type are not immutable.

    """
    pass


class timedelta(object):
    """
    A duration expressing the difference between two date, datetime instances
    to microsecond resolution.

    For data calculations, the calendars of the two date instances must match.

    Objects of this type are not immutable.

    """
    pass


class tzinfo(object):
    """
    An abstract base class for time zone information objects.
    These are used by the datetime and time classes to provide a customizable notion of
    time adjustment (for example, to account for time zone and/or daylight saving time).

    Objects of this type are not immutable.

    """
    pass
