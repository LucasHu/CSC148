# Assignment 1 - Managing students!
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
"""Interactive console for assignment.

This module contains the code necessary for running the interactive console.
As provided, the console does nothing interesting: it is your job to build
on it to fulfill all the given specifications.

run: Run the main interactive loop.
"""

from stack import Stack
from student import Student, Course


def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """
    Master_list = Student()
    command_history = Stack()
    course_list = {}

    while True:
        command = input('')
        if command == 'exit':
            break
        elif command == "":
            print("Unrecognized command!")
            command_history.push("failed")
        else:
            line = command.split()

            # create a student name
            if line[0] == "create" and len(line) == 3:
                if line[1] == "student":
                    create_name(command_history, Master_list, line)
                else:
                    print("Unrecognized command!")
                    command_history.push("failed")

            # enrol a student into a course
            elif line[0] == "enrol" and len(line) == 3:
                enrol_course(course_list, command_history, Master_list, line)

            # drop a student from a course
            elif line[0] == "drop" and len(line) == 3:
                drop_course(course_list, command_history, Master_list, line)

            # list a list of courses a student enrolled
            elif line[0] == "list-courses" and len(line) == 2:
                list_course(course_list, Master_list, line, command_history)

            # list all courses taken by both students
            elif line[0] == "common-courses" and len(line) == 3:
                common_courses(course_list, Master_list, line, command_history)

            # list students enrolled in the course
            elif line[0] == "class-list" and len(line) == 2:
                class_list(course_list, line, command_history)

            # undo, which can reverse the previous command
            elif line[0] == "undo" and len(line) == 1:
                undo(course_list, command_history, Master_list, line)

            # undo(n), which can reverse the last n commands
            elif line[0] == "undo" and len(line) == 2:
                undo_n(course_list, command_history, Master_list, line)

            # if any other commands are given, an error message is given
            else:
                print("Unrecognized command!")
                command_history.push("failed")


def create_name(command_history, Master_list, line):
    """ (command_history,Master_list,line) -> NoneType
    Create student names in the enrollment system based on the input command
    line. If the student already exists, print an ERROR, if not create the
    student name. Each step is stored into a stack, but for an ERROR, a
    "failed" string stored in the stack.

    Parameters:
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list

    """
    if line[2] in Master_list.return_student_name():
        print("ERROR: Student {} already exists.".format(line[2]))
        command_history.push("failed")
    else:
        Master_list.create_student(line[2])
        command_history.push(line)


def enrol_course(course_list, command_history, Master_list, line):
    """ (course_list,command_history,Master_list,line) -> NoneType
    Enrol students into courses. If student hasn't been created, print an
    ERROR. If the course hasn't been created before, create the course and
    then enrol the student inot the course. If the course has been created
    before, enrol the student into the course directly. If the course already
    has 30 people, print a messgae to say the course is full.

    Parameters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list

    """
    if line[1] not in Master_list.return_student_name():
        print("ERROR: Student {} does not exist.".format(line[1]))
        command_history.push("failed")
    elif line[2] not in course_list:
        course_list[line[2]] = Course(line[2])
        course_list[line[2]].enrol(line[1])
        command_history.push(line + ["also_add_course"])
    elif (line[2] in course_list and line[1] not in
          course_list[line[2]].return_enrolled_student()):
        if len(course_list[line[2]].return_enrolled_student()) >= 30:
            print("ERROR: Course {} is full.".format(line[2]))
            command_history.push("failed")
        else:
            course_list[line[2]].enrol(line[1])
            command_history.push(line)
    else:
        command_history.push("failed")


def drop_course(course_list, command_history, Master_list, line):
    """ (course_list,command_history,Master_list,line) -> NoneType
    Remove student names from the course. If the student name hasn't been
    created, print an ERROR. If the student is not in the course, do nothing.

    Parameters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list

    """
    if line[1] not in Master_list.return_student_name():
        print("ERROR: Student {} does not exist.".format(line[1]))
        command_history.push("failed")
    elif (line[2] in course_list and line[1] in
          course_list[line[2]].return_enrolled_student()):
        course_list[line[2]].drop(line[1])
        command_history.push(line)
    else:
        command_history.push("failed")


def list_course(course_list, Master_list, line, command_history):
    """ (course_list,Master_list,line,command_history) -> NoneType
    Print courses taken by a student. If the student has not been created,
    print an ERROR. If the student hasn't enrolled any courses, print a
    message says the student is not taking any courses. Otherwise, print the
    courses taken by the student.

    Parameters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list
    """
    command_history.push("failed")
    if line[1] not in Master_list.return_student_name():
        print("ERROR: Student {} does not exist.".format(line[1]))
    else:
        count = 0
        student_list_courses = []
        for i in range(len(course_list)):
            course_name = list(course_list.keys())[i]
            if line[1] in course_list[course_name].return_enrolled_student():
                count += 1
                student_list_courses.append(course_name)
        if count == 0:
            print("{} is not taking any courses.".format(line[1]))
        else:
            student_list_courses.sort()
            print("{} is taking ".format(line[1]) +
                  ", ".join(str(i) for i in student_list_courses))


def common_courses(course_list, Master_list, line, command_history):
    """ (course_list,Master_list,line,command_history) -> NoneType
    Print the courses taken by two students. If either of the student name
    hasn't been created, print an ERROR. If the two students have no common
    courses, print an empty string.

    Parameters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list
    """
    not_in_count = 0
    command_history.push("failed")
    if line[1] not in Master_list.return_student_name():
        print("ERROR: Student {} does not exist.".format(line[1]))
        not_in_count += 1
    if line[2] not in Master_list.return_student_name():
        print("ERROR: Student {} does not exist.".format(line[2]))
        not_in_count += 1
    if not_in_count == 0:
        common_count = 0
        student_common_course = []
        for i in range(len(course_list)):
            course_name = list(course_list.keys())[i]
            if (line[1] in course_list[course_name].return_enrolled_student()
                and line[2]
                    in course_list[course_name].return_enrolled_student()):
                common_count += 1
                student_common_course.append(course_name)
        if common_count == 0:
                    print("")
        else:
            student_common_course.sort()
            print(", ".join(str(i) for i in student_common_course))


def class_list(course_list, line, command_history):
    """ (course_list,line,command_history) -> NoneType
    Print student names enrolled in a particular course. If no one is taking
    the course, then print a message: No one is taking the course.

    Parameters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    """
    command_history.push("failed")
    if line[1] in course_list:
        if course_list[line[1]].return_enrolled_student() == []:
            print("No one is taking {}.".format(line[1]))
        else:
            course_list[line[1]].return_enrolled_student().sort()
            print(", ".join(str(i) for i in
                            course_list[line[1]].return_enrolled_student()))
    else:
        print("No one is taking {}.".format(line[1]))


def undo(course_list, command_history, Master_list, line):
    """(course_list,command_history,Master_list,line) -> NoneType
    Reverse the last command. The previous command lines were stored in a
    stack, so each time reverse the command line according to the first string
    element. If no command line to reverse, then print a message.

    Paramters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list
    """
    if command_history.is_empty():
        print("ERROR: No commands to undo.")
    else:
        undo_line = command_history.pop()
        if undo_line[0] == "create":
            Master_list.undo_create(undo_line[2])
        elif undo_line[0] == "enrol":
            if len(undo_line) == 4:
                course_list[undo_line[2]].drop(undo_line[1])
                course_list.pop(undo_line[2], None)
            else:
                course_list[undo_line[2]].drop(undo_line[1])
                course_list[undo_line[2]].return_enrolled_student().sort()
        elif undo_line[0] == "drop":
            course_list[undo_line[2]].enrol(undo_line[1])
            course_list[undo_line[2]].return_enrolled_student().sort()


def undo_n(course_list, command_history, Master_list, line):
    """ (course_list,command_history,Master_list,line) -> NoneType
    Reverse the last n lines of command line. If n is not a positive natural
    number, then print a message. If no more command lines, print a message.


    Paramters:
    - course_list: the list stores the name of courses
    - command_history: the stack stores each step
    - Master_list: the list has all student names created in the enrollment
    system
    - line: the input command line was seprated by white space into a list
    """
    try:
        converted_str_int = int(line[1])
        if converted_str_int <= 0:
            print("{} is not a positive natural number.".format(line[1]))
        else:
            for i in range(converted_str_int):
                if command_history.is_empty() is False:
                    undo(course_list, command_history, Master_list, line)
                else:
                    print("ERROR: No commands to undo.")
                    break
    except ValueError:
            print("{} is not a positive natural number.".format(line[1]))

if __name__ == '__main__':
    run()
