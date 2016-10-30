
import unittest

import terra.datetime as datetime


class Testdate(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

class Testtime(unittest.TestCase):
    def test_string(self):
        atime = datetime.time(hour=11, minute=3, second=5)
        self.assertEqual(str(atime), '11:03:05')
        
    def test_string_ms(self):
        atime = datetime.time(hour=3, minute=17, second=25, microsecond=34)
        self.assertEqual(str(atime), '03:17:25.000034')

class Testdate(unittest.TestCase):
    def test_string(self):
        adate = datetime.date(2001,8, 7)
        self.assertEqual(str(adate), '2001-08-07')

if __name__ == '__main__':
    unittest.main()
