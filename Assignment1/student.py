# Assignment 1 - Managing Students!
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
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""


class Student:
    """Student name in the enrollment system.

    The class represents names of students in the enrolment system, which
    supports: add a student name to the list; delete a student name from the
    list and return all student names in the list.

    Attributes:
    - self.student_list (list) : the names of students in the enrollment
    system
    """

    def __init__(self):
        """ (Student) -> NoneType
        Create an empty list as an initial list to store student names

        """
        self.student_list = []

    def create_student(self, student_name):
        """ (Student, str) -> Nonetype
        Add a new student name into the student list

        Parameters:
        - student_name: the name of new student
        """
        self.student_list.append(student_name)

    def undo_create(self, student_name):
        """ (Student, str) -> NoneType
        Remove a student name from the student list

        Paramters:
        - student_name: the name of new student
        """
        self.student_list.remove(student_name)

    def return_student_name(self):
        """ (Student) -> list
        Return the student list with all student names inside
        """

        return self.student_list


class Course:
    """A course in the enrollment system.

    The class represents a course in the enrollment system, and has a list
    that stores the names of students who are enrolled in the course. The
    name(s) of student(s) can be added or removed from the list.

    Attributes:
    - self.course_name (string): the name of the course
    - self.enrolled_student (list): the list of student names that enrolled
    in the course
    """

    def __init__(self, course_name):
        """ (Course) -> Nonetype
        Create a course with correct course name, and also create an empty
        list for this course to store the names of students that enrolled in
        this course.

        Paramters:
        - course_name: the name of the course
        """
        self.course_name = course_name
        self.enrolled_student = []

    def enrol(self, student_name):
        """ (Course) -> Nonetype
        Add the student name into the enrolled student list of this course

        Parameter:
        - student_name: the name of the student
        """
        self.enrolled_student.append(student_name)

    def drop(self, student_name):
        """ (Course) -> Nonetype
        remove the student name from the enrolled student list of this course

        Parameter?
        - student_name: the name of the student
        """
        self.enrolled_student.remove(student_name)

    def return_enrolled_student(self):
        """ (Course) -> list
        Return the list of student names enrolled in this course
        """
        return self.enrolled_student
