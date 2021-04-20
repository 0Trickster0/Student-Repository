"""
This program can read the data of 3 files: students, instructors and grades
, store all the data and display it.
Author: Shengping Xu
"""
import time
from typing import List, DefaultDict, Dict, Iterator
from collections import defaultdict
from prettytable import PrettyTable
import os


class Student:
    """Class to store information of each student"""
    def __init__(self, cwid: str, name: str, major: str) -> None:
        """The initialize function"""
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.grade_dic: Dict[str, str] = {}

    def add_grade(self, course: str, grade: str) -> None:
        """Add or update the grade of a specific course"""
        self.grade_dic[course] = grade


class Instructor:
    """Class to store information of each instructor"""
    def __init__(self, cwid: str, name: str, department: str) -> None:
        """The initialize function"""
        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        # Default dict to store courses and the student number of each course.
        self.course_dic: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course: str) -> None:
        """Add one student to a specific course."""
        self.course_dic[course] += 1


class University:
    """Class that store all the information of a university"""
    def __init__(self, name: str) -> None:
        """The initialize function"""
        self.name = name
        self.students_dic: Dict[str, Student] = {}
        self.instructors_dic: Dict[str, Instructor] = {}

    def pretty_print(self) -> None:
        """Pretty print the information of students and instructors."""
        # Declare two pretty tables with their field names
        student_pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        instructor_pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        # Add the data to pretty tables.
        for student in self.students_dic.values():
            student_pt.add_row([student.cwid, student.name, sorted(student.grade_dic.keys())])
        for instructor in self.instructors_dic.values():
            for course in instructor.course_dic.keys():
                instructor_pt.add_row([instructor.cwid, instructor.name, instructor.department, course,
                                       instructor.course_dic[course]])
        print(f'Student Summary:\n{student_pt}')
        print(f'Instructor Summary: \n{instructor_pt}')


# A university object that store all information
university: University = University("Stevens")


def read_files(file_name: str) -> Iterator[str]:
    """
    Read a file and return each line in order. If error happens, raise an error
    :param file_name: The name of the file
    :return: An iterator of each line
    """
    try:
        fp: IO = open(file_name, 'r')
    # If the file cannot be found, raise an error.
    except FileNotFoundError:
        raise FileNotFoundError(f'There is no {file_name} in the directory.')
    else:
        for line in fp:
            yield line


def main(directory: str = '') -> None:
    """The main function"""
    if not directory:
        directory: str = input('Please input the directory of files: ')
    # Get all the files in the directory
    try:
        # Change the current directory to the specified directory that users enter.
        os.chdir(directory)
    # If the directory is not valid, raise an error
    except FileNotFoundError:
        raise FileNotFoundError(f'{directory} is not a valid directory path.')
    else:
        # Read information of all students
        for line in read_files('students.txt'):
            info: List[str] = line.split()
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 4:
                print(f'The line {line} has wrong number of fields.')
                continue
            cwid: str = info[0]
            name: str = info[1] + info[2]
            major: str = info[3]
            university.students_dic[cwid] = Student(cwid, name, major)
        # Read information of all instructors
        for line in read_files('instructors.txt'):
            info: List[str] = line.split()
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 4:
                print(f'The line {line} has wrong number of fields.')
                continue
            cwid: str = info[0]
            name: str = info[1] + info[2]
            department: str = info[3]
            university.instructors_dic[cwid] = Instructor(cwid, name, department)
        # Read information from grade.txt
        for line in read_files('grades.txt'):
            info: List[str] = line.split()
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 5:
                print(f'The line {line} has a wrong number of fields.')
                continue
            student_id: str = info[0]
            # If the student number is invalid, warn the user and continue processing the next line
            if student_id not in university.students_dic.keys():
                print(f'{student_id} is an unknown student.')
                continue
            instructor_id: str = info[4]
            # If the instructor number is invalid, warn the user and continue processing the next line
            if instructor_id not in university.instructors_dic.keys():
                print(f'{instructor_id} is an unknown instructor.')
                continue
            course: str = f'{info[1]} {info[2]}'
            grade: str = info[3]
            university.students_dic[student_id].add_grade(course, grade)
            university.instructors_dic[instructor_id].add_student(course)
        # Pretty print all the information.
        university.pretty_print()


if __name__ == '__main__':
    main()
