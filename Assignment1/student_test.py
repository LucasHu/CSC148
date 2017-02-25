# Assignment 1 - Unit Tests for Student
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Zhongming (Lucas) Hu, huzhongm
# Chuanqi Sun, sunchuan
# Qing Hui Yu, yuqing1
# ---------------------------------------------
"""Unit tests for student.py

Submit this file, containing *thorough* unit tests
for your code in student.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from student import Student, Course


class TestStudent(unittest.TestCase):
    """Test the functions in student.py

    This class represents a series of tests, which help us to test if
    functions in student.py are working properly.
    """
    def setUp(self):
        """ () -> NoneType
        Set a list to store student names enrolled in the system. Also
        create a subject name.
        """
        self.Master_list = Student()
        self.subject = Course("Chemistry")

    def test_empty_student(self):
        """ () -> NoneType
        Test if initial student name list is an empty list.
        """
        self.assertEqual(self.Master_list.student_list, [])

    def test_create_student(self):
        """ () -> NoneType
        Test if "create_student" function is working properly
        """
        self.Master_list.create_student("David")
        self.assertEqual(self.Master_list.student_list, ["David"])

    def test_undo_create(self):
        """ () -> NoneType
        Test if "undo_create" function is working properly.
        """
        self.Master_list.create_student("David")
        self.Master_list.undo_create("David")
        self.assertEqual(self.Master_list.student_list, [])

    def test_return_student_item(self):
        """ () -> NoneType
        Test if "return_student_name" function is working properly.
        """
        self.Master_list.create_student("David")
        (self.assertEqual(self.Master_list.return_student_name(),
                          self.Master_list.student_list))

    def test_index_create_undo_return(self):
        """ () -> NoneType
        Test if the index is working properly and a few more complicated
        cases.
        """
        self.Master_list.create_student("David")
        self.Master_list.create_student("Lucas")
        self.Master_list.create_student("Philip")
        self.assertEqual(self.Master_list.student_list[2], "Philip")
        self.Master_list.undo_create("Philip")
        (self.assertRaises(IndexError,
                           self.Master_list.student_list.__getitem__, 2))
        self.assertEqual(self.Master_list.student_list, ["David", "Lucas"])

    def test_course_name_enrolled_student(self):
        """ () -> NoneType
        Test if the intial attributes are set correctly.
        """
        self.assertEqual(self.subject.course_name, "Chemistry")
        self.assertEqual(self.subject.enrolled_student, [])

    def test_enrol(self):
        """ () -> NoneType
        Test if function "enrol" is working properly.
        """
        self.subject.enrol("David")
        self.assertEqual(self.subject.enrolled_student, ["David"])

    def test_drop(self):
        """ () -> NoneType
        Test if function "drop" is working properly.
        """
        self.subject.enrol("David")
        self.subject.drop("David")
        self.assertEqual(self.subject.enrolled_student, [])

    def test_return_enrolled_student(self):
        """ () -> NoneType
        Test if function "return_enrolled_student" is working properly.
        """
        self.subject.enrol("David")
        self.subject.drop("David")
        self.subject.enrol("Lucas")
        (self.assertEqual(self.subject.return_enrolled_student(),
                          self.subject.enrolled_student))

    def test_index_enrol_drop_return(self):
        """ () -> NoneType
        Test if the index is working properly and a few more complicated
        cases.
        """
        self.subject.enrol("David")
        self.subject.enrol("Lucas")
        self.subject.enrol("Philip")
        self.assertEqual(self.subject.enrolled_student[2], "Philip")
        self.subject.drop("David")
        self.assertEqual(self.subject.enrolled_student[0], "Lucas")
        (self.assertRaises(IndexError,
                           self.subject.enrolled_student.__getitem__, 2))
        self.assertEqual(self.subject.enrolled_student, ["Lucas", "Philip"])

if __name__ == '__main__':
    unittest.main(exit=False)
