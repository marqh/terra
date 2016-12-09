
import unittest

import numpy as np
import datetime
import terra.datetime


class Testtime(unittest.TestCase):
    def test_string(self):
        atime = datetime.time(hour=11, minute=3, second=5)
        ttime = terra.datetime.time(hour=11, minute=3, second=5)
        self.assertEqual(str(atime), str(ttime))
        
    def test_string_ms(self):
        atime = datetime.time(hour=3, minute=17, second=25, microsecond=34)
        ttime = terra.datetime.time(hour=3, minute=17, second=25, microsecond=34)
        self.assertEqual(str(atime), str(ttime))
        
class Testdate(unittest.TestCase):
    def test_string(self):
        adate = datetime.date(2001, 8, 7)
        tdate = terra.datetime.date(2001, 8, 7)
        self.assertEqual(str(adate), str(tdate))

class TestDatePlusMinus(unittest.TestCase):
    def test_days(self):
        adate = datetime.date(2001, 8, 7)
        bdate = datetime.date(2001, 9, 7)
        delta = bdate - adate
        tadate = terra.datetime.date(2001, 8, 7)
        tbdate = terra.datetime.date(2001, 9, 7)
        tdelta = tbdate - tadate
        exptd = 31
        msg = '{} != {} != {}'.format(tdelta.days, delta.days, exptd)
        self.assertTrue(tdelta.days == delta.days == exptd, msg=msg)

    def test_days_months(self):
        adate = datetime.date(2001, 8, 7)
        bdate = datetime.date(2001, 11, 17)
        delta = bdate - adate
        tadate = terra.datetime.date(2001, 8, 7)
        tbdate = terra.datetime.date(2001, 11, 17)
        tdelta = tbdate - tadate
        exptd = 102
        msg = '{} != {} != {}'.format(tdelta.days, delta.days, exptd)
        self.assertTrue(tdelta.days == delta.days == exptd, msg=msg)

    def test_days_ten_years(self):
        adate = datetime.date(2001, 8, 7)
        bdate = datetime.date(2011, 9, 7)
        delta = bdate - adate
        tadate = terra.datetime.date(2001, 8, 7)
        tbdate = terra.datetime.date(2011, 9, 7)
        tdelta = tbdate - tadate
        exptd = 3683
        msg = '{} != {} != {}'.format(tdelta.days, delta.days, exptd)
        self.assertTrue(tdelta.days == delta.days == exptd, msg=msg)

    def test_days_ten_years_days(self):
        adate = datetime.date(2001, 8, 7)
        exp_bdate = datetime.date(2011, 9, 7)
        bdate = adate + datetime.timedelta(days=3683)
        tadate = terra.datetime.date(2001, 8, 7)
        texpbdate = terra.datetime.date(2011, 9, 7)
        tbdate = tadate + terra.datetime.timedelta(days=3683)
        self.assertEqual(str(bdate), str(tbdate))

    def test_days_two_years(self):
        adate = datetime.date(2001, 8, 7)
        bdate = datetime.date(2003, 9, 7)
        delta = bdate - adate
        tadate = terra.datetime.date(2001, 8, 7)
        tbdate = terra.datetime.date(2003, 9, 7)
        tdelta = tbdate - tadate
        exptd = 761
        msg = '{} != {} != {}'.format(tdelta.days, delta.days, exptd)
        self.assertTrue(tdelta.days == delta.days == exptd, msg=msg)

class TestDatetime(unittest.TestCase):
    def test_total_seconds(self):
        adate = datetime.datetime(2001, 8, 7)
        bdate = datetime.datetime(2001, 9, 7)
        delta = bdate - adate
        tadate = terra.datetime.datetime(2001, 8, 7)
        tbdate = terra.datetime.datetime(2001, 9, 7)
        tdelta = tbdate - tadate
        exptd = 2678400
        msg = '{} != {} != {}'.format(tdelta.total_seconds(), delta.total_seconds(), exptd)
        self.assertTrue(tdelta.total_seconds() == delta.total_seconds() == exptd, msg=msg)

    def test_total_seconds_two_years(self):
        adate = datetime.datetime(2001, 8, 7)
        bdate = datetime.datetime(2003, 9, 7)
        delta = bdate - adate
        tadate = terra.datetime.datetime(2001, 8, 7)
        tbdate = terra.datetime.datetime(2003, 9, 7)
        tdelta = tbdate - tadate
        exptd = 65750400
        msg = '{} != {} != {}'.format(tdelta.total_seconds(), delta.total_seconds(), exptd)
        self.assertTrue(tdelta.total_seconds() == delta.total_seconds() == exptd, msg=msg)

class TestIntegerDatetimeOffset(unittest.TestCase):
    def test_days_offset(self):
        adate = datetime.date(2001, 8, 7)
        bdate = adate + datetime.timedelta(days=3683)
        tdate = terra.datetime.date(2001, 8, 7)
        edate = terra.datetime.EpochDateTimes(np.array((3683,)), 'day', epoch=tdate)
        self.assertEqual(str(bdate), str(edate))
        

if __name__ == '__main__':
    unittest.main()
