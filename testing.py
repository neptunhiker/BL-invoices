import datetime
import unittest

from avgs import AVGSCoupon
from helpers import format_to_german_date, determine_payment_target_date
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


class TestsFormatDate(unittest.TestCase):

    def test_format_date(self):
        date = datetime.date(year=1984, month=1, day=31)
        target_output = "31. Januar 1984"
        func_output = format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=1990, month=2, day=1)
        target_output = "01. Februar 1990"
        func_output = format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=3, day=9)
        target_output = "09. März 2021"
        func_output = format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=8, day=4)
        target_output = "04. August 2021"
        func_output = format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=10, day=19)
        target_output = "19. Oktober 2021"
        func_output = format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

    def test_bad_input(self):
        date = "2021-06-03"
        target_output = f"Cannot format date {date}"
        func_output = format_to_german_date(date)
        self.assertEqual(func_output, target_output)


class TestsPaymentHorizon(unittest.TestCase):

    def test_payment_target_date(self):
        date = datetime.date(year=2021, month=2, day=26)
        target_output = datetime.date(year=2021, month=3, day=12)
        func_output = determine_payment_target_date(date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=12, day=23)
        target_output = datetime.date(year=2022, month=1, day=6)
        func_output = determine_payment_target_date(date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=10, day=16)
        target_output = datetime.date(year=2021, month=11, day=1)
        func_output = determine_payment_target_date(date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2022, month=1, day=12)
        target_output = datetime.date(year=2022, month=1, day=31)
        func_output = determine_payment_target_date(date=date, payment_horizon_in_days=17)
        self.assertEqual(func_output, target_output)

    def test_bad_input(self):
        date = "2021-05-12"
        payment_horizon_in_days = 14
        self.assertRaises(Exception, determine_payment_target_date, date, payment_horizon_in_days)

        date = "some string"
        payment_horizon_in_days = 14
        self.assertRaises(Exception, determine_payment_target_date, date, payment_horizon_in_days)

        date = datetime.date(year=2022, month=1, day=12)
        payment_horizon_in_days = "14"
        self.assertRaises(Exception, determine_payment_target_date, date, payment_horizon_in_days)


if __name__ == '__main__':
    unittest.main()
