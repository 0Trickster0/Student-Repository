"""
This program can read the data of 3 files: students, instructors and grades
, store all the data and display it.
Author: Shengping Xu
"""
from typing import List, DefaultDict, Dict, Iterator, IO
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
        self.remain_R: List[str] = list(university.majors_dic[self.major].required_courses)
        self.remain_E: List[str] = list(university.majors_dic[self.major].elective_courses)
        self.grade_dic: Dict[str, str] = {}

    def add_grade(self, course: str, grade: str) -> None:
        """Add or update the grade of a specific course"""
        if course in self.remain_E:
            # If a student has completed an elective course, he does not need to complete another elective course
            self.remain_E.clear()
        elif course in self.remain_R:
            # If a student has completed a required course, delete the course
            self.remain_R.remove(course)
        self.grade_dic[course] = grade

    def calculate_gpa(self) -> float:
        # Calculate the overall GPA of a student
        def convert_grade(grade: str) -> float:
            if grade == 'A':
                return 4
            elif grade == 'A-':
                return 3.75
            elif grade == 'B+':
                return 3.25
            elif grade == 'B':
                return 3
            elif grade == 'B-':
                return 2.75
            elif grade == 'C+':
                return 2.25
            elif grade == 'C':
                return 2
            else:
                return 0
        # If the student does not have any grades, return 0
        if not self.grade_dic:
            print(f'Student {self.name} does not have any grades.')
            return 0
        total_grade: float = 0
        for g in self.grade_dic.values():
            total_grade += convert_grade(g)
        # Round the final result to 2 digits
        return (total_grade / len(self.grade_dic)).__round__(2)


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


class Major:
    """Class to store information of each major"""
    def __init__(self, name: str) -> None:
        """The initialize function"""
        self.name: str = name
        self.required_courses: List[str] = []
        self.elective_courses: List[str] = []

    def add_course(self, course: str, is_required: bool) -> None:
        """Add courses to required courses or elective courses"""
        if is_required:
            self.required_courses.append(course)
        else:
            self.elective_courses.append(course)


class University:
    """Class that store all the information of a university"""
    def __init__(self, name: str) -> None:
        """The initialize function"""
        self.name = name
        self.students_dic: Dict[str, Student] = {}
        self.instructors_dic: Dict[str, Instructor] = {}
        self.majors_dic: Dict[str, Major] = {}

    def pretty_print(self) -> None:
        """Pretty print the information of students and instructors."""
        # Declare two pretty tables with their field names
        student_pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses',
                                                           'Remaining Required', 'Remaining Electives', 'GPA'])
        instructor_pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        major_pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])
        # Add the data to pretty tables.
        for major in self.majors_dic.values():
            major_pt.add_row([major.name, sorted(major.required_courses), sorted(major.elective_courses)])
        for student in self.students_dic.values():
            student_pt.add_row([student.cwid, student.name, student.major, sorted(student.grade_dic.keys()),
                                sorted(student.remain_R), sorted(student.remain_E), student.calculate_gpa()])
        for instructor in self.instructors_dic.values():
            for course in instructor.course_dic.keys():
                instructor_pt.add_row([instructor.cwid, instructor.name, instructor.department, course,
                                       instructor.course_dic[course]])
        print(f'Majors summary: \n{major_pt}')
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
        # A header boolean value to skip headers in each file
        header = True
        # Read information of majors
        for line in read_files('majors.txt'):
            if header:
                header = False
                continue
            line = line.strip('\n')
            info: List[str] = line.split('\t')
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 3:
                print(f'The line {line} has a wrong number of fields.')
                continue
            major: str = info[0]
            is_required: bool = info[1] == 'R'
            course: str = info[2]
            if not university.majors_dic.__contains__(major):
                university.majors_dic[major] = Major(major)
            university.majors_dic[major].add_course(course, is_required)
        header: bool = True
        # Read information of all students
        for line in read_files('students.txt'):
            if header:
                header = False
                continue
            line = line.strip('\n')
            info: List[str] = line.split('\t')
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 3:
                print(f'The line {line} has wrong number of fields.')
                continue
            cwid: str = info[0]
            name: str = info[1]
            major: str = info[2]
            university.students_dic[cwid] = Student(cwid, name, major)
        # Read information of all instructors
        header = True
        for line in read_files('instructors.txt'):
            if header:
                header = False
                continue
            line = line.strip('\n')
            info: List[str] = line.split('\t')
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 3:
                print(f'The line {line} has wrong number of fields.')
                continue
            cwid: str = info[0]
            name: str = info[1]
            department: str = info[2]
            university.instructors_dic[cwid] = Instructor(cwid, name, department)
        # Read information from grade.txt
        header = True
        for line in read_files('grades.txt'):
            if header:
                header = False
                continue
            line = line.strip('\n')
            info: List[str] = line.split('\t')
            # If the field number is wrong, warn the user and continue processing the next line
            if len(info) != 4:
                print(f'The line {line} has a wrong number of fields.')
                continue
            student_id: str = info[0]
            # If the student number is invalid, warn the user and continue processing the next line
            if student_id not in university.students_dic.keys():
                print(f'{student_id} is an unknown student.')
                continue
            instructor_id: str = info[3]

            # If the instructor number is invalid, warn the user and continue processing the next line
            if instructor_id not in university.instructors_dic.keys():
                print(f'{instructor_id} is an unknown instructor.')
                continue
            course: str = info[1]
            grade: str = info[2]
            if grade != 'A' and grade != 'A-' and grade != 'B+' and grade != 'B' and grade != 'B-' \
                    and grade != 'C+' and grade != 'C':
                continue
            university.students_dic[student_id].add_grade(course, grade)
            university.instructors_dic[instructor_id].add_student(course)
        # Pretty print all the information.
        university.pretty_print()


if __name__ == '__main__':
    main()
