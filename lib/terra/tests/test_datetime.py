
import unittest
import numpy as np

import terra.datetime as datetime


class Testtime(unittest.TestCase):
    def test_string(self):
        atime = datetime.time(hour=11, minute=3, second=5)
        self.assertEqual(str(atime), '11:03:05')
        
    def test_string_ms(self):
        atime = datetime.time(hour=3, minute=17, second=25, microsecond=34)
        self.assertEqual(str(atime), '03:17:25.000034')

class Testdate(unittest.TestCase):
    def test_string(self):
        adate = datetime.date(2001, 8, 7)
        self.assertEqual(str(adate), '2001-08-07')

class TestOffset(unittest.TestCase):
    def test_many_seconds(self):
        origin = '1970-01-01 00:00:00Z'
        ig = datetime.ISOGregorian()
        tog = datetime.parse_datetime(origin, calendar=ig)
        sample = datetime.EpochDateTimes(np.array(1513673731),
                                         'second', epoch=tog)
        self.assertEqual(str(sample), '2017-12-19T08:55:03')

    def test_array_seconds(self):
        origin = '1970-01-01 00:00:00Z'
        ig = datetime.ISOGregorian()
        tog = datetime.parse_datetime(origin, calendar=ig)
        sample = datetime.EpochDateTimes(np.array((1513673731, 1513673735)),
                                         'second', epoch=tog)
        self.assertEqual(str(sample),
                         "['2017-12-19T08:55:03' '2017-12-19T08:55:07']")


class Testtimedelta(unittest.TestCase):
    def test_foo(self):
        pass

if __name__ == '__main__':
    unittest.main()
