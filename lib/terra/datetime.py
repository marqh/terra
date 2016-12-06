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
import copy


class date(object):
    """
    An idealized naive date,  Attributes: year, month, and day.

    Objects of this type are not immutable.

    """
    def __init__(self, year, month, day, calendar=None):
        self.year = year
        self.month = month
        self.day = day
        self.calendar = calendar

    def __str__(self):
        return '{0:0>4}-{1:0>2}-{2:0>2}'.format(self.year, self.month,
                                                self.day)

    def __repr__(self):
        return 'terra.datetime.date({}, {}, {})'.format(self.year,
                                                        self.month,
                                                        self.day)

    def __sub__(self, other):
        return Duration(self, other)

    def __add__(self, other):
        #if not isinstance(other, DateDuration):
        if not isinstance(other, timedelta):
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            msg = msg.format(type(self), type(other))
            raise TypeError(msg)
        if other.seconds is not None or other.microseconds is not None:
            raise ValueError('Neither seconds nor microseconds may be added to a date.')
        if other.days is None:
            raise ValueError('Adding None days to a date is not supported.')
        # if self.calendar != other.calendar:
        #     import pdb; pdb.set_trace()
        #     raise ValueError('Calendars must be the same for additions.')
        if self.calendar is None:
            calendar = GregorianNoLeapSecond()
        else:
            calendar = self.calendar
        # if other.year is not None:
        #     newyear = self.year + other.year
        # else:
        #     newyear = self.year
        # if other.month is not None:
        #     newmonth = self.month + other.month
        #     if newmonth > calendar.months_in_year:
        #         newyear += 1
        #         newmonth = newmonth - calendar.months_in_year
        # else:
        #     newmonth = self.month
        # if other.day is not None:
        #     if other.month is not None:
        #         if other.day > calendar.month_day_map[other.month]:
        #             if calendar.is_leap_year(newyear) and newmonth == calendar.leap_year_date.month:
        #                 if other.day > calendar.month_day_map[other.month] + 1:
        #                     msg = 'Day value {} outside month range {}.'
        #                     msg = msg.format(other.day, calendar.month_day_map[other.month])
        #                     raise ValueError(msg)
        #     newday = self.day
        #     for day in range(other.day):
        #         newday = newday + 1
        #         days_in_month = calendar.month_day_map[newmonth]
        #         if calendar.is_leap_year(newyear) and newmonth == calendar.leap_year_date.month:
        #             days_in_month += 1
        #         if newday > days_in_month:
        #             newday = newday - days_in_month
        #             newmonth += 1
        #             if newmonth > calendar.months_in_year:
        #                 newyear += 1
        #                 newmonth = newmonth - calendar.months_in_year
                
        # else:
        #     newday = self.day

        newyear = self.year
        newmonth = self.month
        newday = self.day
        for day in range(other.days):
            newday = newday + 1
            days_in_month = calendar.month_day_map[newmonth]
            if calendar.is_leap_year(newyear) and newmonth == calendar.leap_year_date.month:
                days_in_month += 1
            if newday > days_in_month:
                newday = newday - days_in_month
                newmonth += 1
                if newmonth > calendar.months_in_year:
                    newyear += 1
                    newmonth = newmonth - calendar.months_in_year
        
        return date(newyear, newmonth, newday, self.calendar)

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

        # Design question: validate inputs?
        self.date = date(year, month, day, calendar)
        self.time = time(hour, minute, second, microsecond, tzinfo)

    def __sub__(self, other):
        return Duration(self, other)

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

    @property
    def calendar(self):
        return self.date.calendar

    @property
    def hour(self):
        return self.time.hour

    @property
    def minute(self):
        return self.time.minute

    @property
    def second(self):
        return self.time.second

    @property
    def microsecond(self):
        return self.time.microsecond

    @property
    def tzinfo(self):
        return self.time.tzinfo

class Duration(object):
    """
    Represents a temporal period between two date or two datetime instances.

    The calendars of the two date or datetime instances must
    match.
    If both calendars are None, a GregorianNoLeapSecond
    calendar is assumed.  This is intended to give consistent results
    with Python's datetime module in most cases.

    """
    def __init__(self, end, start):
        if start.calendar != end.calendar:
            raise ValueError('Duratons are not well defined across differing calendars '
                             'for terra.datetime instances.')
        if start.calendar is None:
            self.calendar = GregorianNoLeapSecond()
        else:
            self.calendar = start.calendar
        self.start = start
        self.end = end

    # @property
    # def resolution(self):
        # return another time delta

    @property
    def years(self):
        """Return the length of time, floored to the nearest year."""
        if self.start.year is None or self.end.year is None:
            result = None
        else:
            result = self.end.year - self.start.year
            if self.end.month < self.start.month:
                if not self.end.day < self.start.day:
                    result -= 1
        return result
        
    # @property
    # def months(self):
    #     # requires that the calendars are not None and the number of months per year
    #     if self.start.year is None or self.end.year is None:
    #         result = None
    #     else:
    #         result = self.end.year - self.start.year
    #     return result
        
    @property
    def days(self):
        """Return the floor of the number of days."""
        def _add_day(adate, days):
            adate = adate + timedelta(days=1)
            days += 1
            if (self.calendar.is_leap_year(adate.year) and
                adate.month == self.calendar.leap_year_date.month and
                adate.day == (self.calendar.leap_year_date.day - 1)):
                days += 1
                adate = adate + timedelta(days=1)
            return adate, days

        if self.start.day is None or self.end.day is None:
            result = None
        else:
            # Accumulate to calculate
 
            adate = copy.copy(self.start)
            days = 0
            for d in range(self.calendar.month_day_map[self.start.month])[self.start.day:]:
                adate, days = _add_day(adate, days)
            if self.end.year == self.start.year:
                if self.end.month - self.start.month > 1:
                    for month_length in self.calendar.month_day_map[self.start.month:self.end.month]:
                        for d in range(month_length):
                            adate, days = _add_day(adate, days)
            else:

                for month_length in self.calendar.month_day_map[self.start.month + 1:]:
                    for d in range(month_length):
                        adate, days = _add_day(adate, days)
                for year in range(self.end.year - self.start.year -1):
                    for month_length in self.calendar.month_day_map:
                        for d in range(month_length):
                            adate, days = _add_day(adate, days)
                for month_length in self.calendar.month_day_map[:self.end.month]:
                    for d in range(month_length):
                        adate, days = _add_day(adate, days)
            for d in range(self.calendar.month_day_map[self.end.month])[:self.end.day]:
                adate, days = _add_day(adate, days)
            result = days
        return result
        
        
        
    def total_hours(self):
        if self.start.hour is None or self.end.hour is None:
            result = None
        else:
            hours = self.end.hour - self.start.hour
            result = self.days() * 24 + hours
        return result
        
    def total_minutes(self):
        if self.start.minute is None or self.end.minute is None:
            result = None
        else:
            minutes = self.end.minute - self.start.minute
            result = self.total_hours() * 60 + minutes
        return result

    @property
    def seconds(self):
        if self.start.second is None or self.end.second is None:
            result = None
        else:
            seconds = self.end.second - self.start.second
            result = self.total_minutes() * 60 + seconds
        if False:
            # handle leap seconds if they exist within the period
            leapseconds = 0
            result += 1 * leapseconds

        return result

    def total_seconds(self):
        tsec = self.seconds
        if tsec is not None and self.microseconds is not None:
            result = self.seconds + self.microseconds
        return result

    @property
    def microseconds(self):
        if self.start.microsecond is None or self.end.microsecond is None:
            result = None
        else:
            microseconds = self.end.microsecond - self.start.microsecond
            result = self.start.seconds() * 1e6 + microseconds
        return result


class tzinfo(object):
    """
    An abstract base class for time zone information objects.
    These are used by the datetime and time classes to provide a customizable
    notion of time adjustment (for example, to account for time zone and/or
    daylight saving time).

    Objects of this type are not immutable.

    """
    pass

class timedelta(object):
    def __init__(self, days=None, seconds=None, microseconds=None):
        self.days = days
        self.seconds = seconds
        self.microseconds = microseconds

    def total_seconds(self):
        return None


class DateDuration(Duration):
    """
    A datetime duration, represented by whole unit like quantities.

    For example 'April, 2012, ISO-Gregorian' is the whole month of April
    with respect to the ISO-Gregorian Calendar.

    Elements may be None, in which case the duration refers to any value
    for that element.

    """
    def __init__(self, year=None, month=None, day=None, calendar=None):
        self.year = year
        self.month = month
        self.day = day
        self.calendar = calendar

    def __sub__(self, other):
        return Duration(self, other)



class TimeDuration(Duration):
    """
    A datetime duration, represented by whole unit like quantities.

    For example 'April, 2012, ISO-Gregorian' is the whole month of April
    with respect to the ISO-Gregorian Calendar.

    Elements may be None, in which case the duration refers to any value
    for that element.

    """
    def __init__(self, hour=None, minute=None, second=None):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __sub__(self, other):
        return Duration(self, other)



# class SegmentedDuration(object):
#     """
#     A datetime duration, represented by collections of unit like quantities.
#     The duration may be segmented, for example: particular months within
#     particular years.

#     All defined elements match.
    

#     """
#     def __init__(self, year=None, month=None, day=None, hour=None,
#                  calendar=None):
#         self.years = year
#         self.months = month
#         self.days = day
#         self.hours = hour
#         self.calendar = calendar


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
                 leap_year_date=None,
                 months_in_year=None, month_names=None,
                 month_day_map=None, leapsecond_datetimes=None,
                 days_in_week=None, weekday_names=None,
                 weekday_start_date=None):
        self.url = url
        self.days_in_year = days_in_year
        self.days_in_leap_year = days_in_leap_year
        self.leap_year_date = leap_year_date
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

        def is_leap_year(year):
            """Return True for leap years, False for non-leap years."""
            return False    

class GregorianNoLeapSecond(Calendar):
    def __init__(self):
        url = None


        leap_year_date = date(None, 2, 29)
        #generator
        leap_year_years = []
        months_in_year = 12
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_day_map = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_in_year = sum(month_day_map)
        days_in_leap_year = days_in_year + 1
        leapsecond_datetimes = None
        days_in_week = 7
        weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekday_start_date = date(1995, 1, 1)

        super(GregorianNoLeapSecond, self).__init__(url, days_in_year, days_in_leap_year,
                                                    leap_year_date,
                                                    months_in_year, month_names,
                                                    month_day_map, leapsecond_datetimes,
                                                    days_in_week, weekday_names,
                                                    weekday_start_date)
    def is_leap_year(self, year):
        """Return True for leap years, False for non-leap years."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
