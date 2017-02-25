import unittest

from planner import TermPlanner, parse_course_data
from course import Course


class TestParser(unittest.TestCase):

    def test_binary_simple(self):
        filename = 'binary_simple.txt'

        actual = parse_course_data(filename)
        self.assertEqual('CSC207', actual.name)