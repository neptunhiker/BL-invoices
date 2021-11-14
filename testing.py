import datetime
import unittest

from avgs import AVGSCoupon
from participants import Participant


class TestsParticipants(unittest.TestCase):

    def setUp(self) -> None:
        self.joe = Participant(first_name="Joe", last_name="Doe")

    def test_last_name_change(self):
        self.joe.last_name = "Richardson"
        self.assertEqual(self.joe.last_name, "Richardson")
        self.assertEqual(self.joe.full_name, "Joe Richardson")

    def test_first_name_change(self):
        self.joe.first_name = "Ben"
        self.assertEqual(self.joe.first_name, "Ben")
        self.assertEqual(self.joe.full_name, "Ben Doe")

    def test_full_name_change(self):
        pass
        # how to implement that this is not allowed?

    def test_full_name(self):
        self.assertEqual(self.joe.full_name, "Joe Doe")


class TestsAVGS(unittest.TestCase):

    def setUp(self) -> None:
        self.avgs = AVGSCoupon(avgs_nr="asdfjklo-6", time_period_start=datetime.date(2021, 11, 19),
                               time_period_end=datetime.date(2022, 1, 22))

    def test_change_start_date(self):
        self.avgs.time_period_start = datetime.date(2022, 1, 10)
        self.assertEqual(self.avgs.time_period_length, 12)

    def test_change_end_date(self):
        self.avgs.time_period_end = datetime.date(2021, 12, 9)
        self.assertEqual(self.avgs.time_period_length, 20)


if __name__ == '__main__':
    unittest.main()
