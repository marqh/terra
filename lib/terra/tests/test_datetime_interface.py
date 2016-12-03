
import unittest

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

class Testtimedelta(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
