
import unittest

import numpy as np

import terra
import terra.datetime


class TestIntegerDatetimeOffsetUTC(unittest.TestCase):
    def test_days_offset(self):
        tdate = terra.datetime.datetime(2001, 8, 7, calendar=terra.datetime.ISOGregorian())
        edate = terra.datetime.EpochDateTimes(np.array((3683,)), 'day', epoch=tdate)
        edate = terra.datetime.EpochDateTimes(np.array((3683 * 86400.0 + 2,)), 'second', epoch=tdate)
        tcrs_str = ('TIMECRS["GPS Time",'
                    'TDATUM["Time origin",TIMEORIGIN[2001-08-07T00:00:00.0Z]],'
                    'CS[temporal,1],AXIS["time",future],TIMEUNIT["day",86400.0]]')
        tcrs = terra.parse_wktcrs(tcrs_str)
        time_values = np.array((3683,))
        self.assertEqual(str(edate), tcrs.datetime_strings(time_values))

    def test_days_offset_ten_years(self):
        tdate = terra.datetime.datetime(2001, 8, 7, calendar=terra.datetime.ISOGregorian())
        edate = terra.datetime.EpochDateTimes(np.array((318211200,)), 'second', epoch=tdate)
        tcrs_str = ('TIMECRS["GPS Time",'
                    'TDATUM["Time origin",TIMEORIGIN[2001-08-07T00:00:00.0Z]],'
                    'CS[temporal,1],AXIS["time",future],TIMEUNIT["second",1.0]]')
        tcrs = terra.parse_wktcrs(tcrs_str)
        time_values = np.array((318211200,))
        self.assertEqual(str(edate), tcrs.datetime_strings(time_values))

    def test_days_offset_ten_years_hours(self):
        tdate = terra.datetime.datetime(2001, 8, 7, calendar=terra.datetime.ISOGregorian())
        edate = terra.datetime.EpochDateTimes(np.array((318211200 + 33333,)), 'second', epoch=tdate)
        tcrs_str = ('TIMECRS["GPS Time",'
                    'TDATUM["Time origin",TIMEORIGIN[2001-08-07T00:00:00.0Z]],'
                    'CS[temporal,1],AXIS["time",future],TIMEUNIT["second",1.0]]')
        tcrs = terra.parse_wktcrs(tcrs_str)
        time_values = np.array((318211200 + 33333,))
        self.assertEqual(str(edate), tcrs.datetime_strings(time_values))



if __name__ == '__main__':
    unittest.main()
