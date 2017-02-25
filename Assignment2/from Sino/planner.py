# Assignment 2 - Course Planning!
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
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import Course


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    courses = {}
    with open(filename, 'r') as source:
        for line in source:
            classes = line.split()
            if classes[0] not in courses:
                courses[classes[0]] = Course(classes[0])
            if classes[1] not in courses:
                courses[classes[1]] = Course(classes[1])
            courses[classes[1]].add_prereq(courses[classes[0]])
    return get_top(courses)


class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        course_taken = []
        if schedule == []:
            return True
        else:
            if check_validity(schedule, course_taken, self.course) is False:
                restore(self.course)  # if it's not valid, return false
                return False
            elif repeats(course_taken):  # if it contains repeating element
                restore(self.course)    # return false
                return False
            restore(self.course)
            return True

    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.

        You may assume that all the courses in selected_courses appear in
        self.course.

        If no valid schedule can be formed from these courses, return an
        empty list.
        """
        copy_want = selected_courses[:]
        for cour in copy_want:
            if cour not in self.course:
                return []
        schedule = []
        while add_possible_schedule(schedule, copy_want, self.course):
            pass    # while add_possible doesn't return [], keep generating
        if len(copy_want) != 0:
            return []  # if there are remaining, the schedule can'e be formed
        restore(self.course)
        if self.is_valid(schedule):  # check if the schedule is valid
            return schedule
        else:
            return []


def get_top(courses):
    """ (Dictionary of Courses) -> Course

    Return the topmost course in a course dictionary, a topmost course
    is defined as the course that does not appear in any other course's
    prereq list.
    """
    for cour in courses:
        is_top = True
        for compare in courses:  # false if it's some other's prereq
            if courses[cour] in courses[compare].prereqs:
                is_top = False
        if is_top:
            return courses[cour]


def repeats(lst):
    """ (lst of str) -> bool

    Return True if the list contains repeating elements, false otherwise.
    """
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


def restore(course):
    """ (Course) -> NoneType

    Restore a course tree and all its subtrees to an untaken state.
    """
    course.taken = False
    for prereq in course.prereqs:  # change all taken to false
        restore(prereq)


def take(code, course):
    """ (str, Course) -> NoneType

    Find the course in a course tree by name and take it.
    """
    if course.name == code:
        course.take()
    elif course.prereqs == []:
        pass
    else:
        for cour in course.prereqs:
            take(code, cour)  # find the course in tree


def prereqs_taken(code, course):
    """ (str, Course) -> bool

    Find a course in a course tree, and return True if all the prereqs of
    the course is taken, false otherwise.
    """
    if course.name == code:
        return course.is_takeable()
    elif course.prereqs == []:
        return True
    else:
        for cour in course.prereqs:
            if not prereqs_taken(code, cour):
                return False  # false if the course is not takeable
        return True


def check_validity(schedule, taken, course_tree):
    """ (lst of (list of str), list of str, Course) -> Bool

    Check if the courses in schedule in in the Coursetree, and check if every
    course in schedule is taken after all the prereqs are taken, return False
    if either is False, True if every course in schedule exists and are taken
    in an acceptable order.
    """
    for sch in schedule:  # read the terms
        taking = []
        for cour in sch:  # read the courses
            if cour not in course_tree:
                return False
            else:
                if prereqs_taken(cour, course_tree):
                    taking.append(cour)
                else:
                    return False
        for item in taking:  # take the course and add it to taken
            take(item, course_tree)
            taken.append(item)
    return True


def add_possible_schedule(schedule, selected, course_tree):
    """ (lst of (list of str), list of str, Course) -> NoneType

    Find possible schedule based on the taken status of the courses,
    generate a one-term schedule, and add it to the schedule list.
    """
    sch = []  # the semester schedule
    for cour in selected:
        if prereqs_taken(cour, course_tree) and len(sch) < 5:
            sch.append(cour)
    for course in sch:
        take(course, course_tree)  # take it and
        selected.remove(course)  # remove it from selected list
    sch.sort()
    if sch != []:
        schedule.append(sch)
        return True
    else:
        return False
