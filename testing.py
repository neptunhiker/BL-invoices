import unittest

from participants import Participant


class TestsParticipants(unittest.TestCase):

    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()
