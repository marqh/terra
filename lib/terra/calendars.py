import terra.datetime

def gregorian_no_leap():
    """:mod:`terra.datetime.Calendar` factory, returning a gregorian calendar with no leap seconds defined."""
    url = None
    
    
    leap_year_date = terra.datetime.date(None, 2, 29)
    #generator
    leap_year_years = []
    months_in_year = 12
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_day_map = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_year = sum(month_day_map)
    days_in_leap_year = days_in_year + 1
    leapsecond_datetimes = None
    days_in_week = 7
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday_start_date = terra.datetime.date(1995, 1, 1)

    gcal = terra.datetime.Calendar(url, days_in_year, days_in_leap_year,
                                   leap_year_date, leap_year_years,
                                   months_in_year, month_names,
                                   month_day_map, leapsecond_datetimes,
                                   days_in_week, weekday_names,
                                   weekday_start_date)
    return gcal
