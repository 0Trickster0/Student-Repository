"""
This file in a unit test file for homework 9
Author: Shengping Xu
"""
import unittest
import Student_Repository_Shengping_Xu as hw


class FileSummarizeTestCase(unittest.TestCase):
    """Test class to test the classes and functions in homework 9"""
    def test_file_summarize(self) -> None:
        """Test cases to test the classes and functions in homework 9"""
        hw.main()
        self.assertEqual(hw.university.students_dic['10103'].name, 'Jobs, S')
        self.assertEqual(hw.university.students_dic['10115'].name, 'Bezos, J')
        self.assertEqual(hw.university.instructors_dic['98764'].name, 'Cohen, R')
        self.assertEqual(hw.university.instructors_dic['98762'].name, 'Hawking, S')
        # Test if the data retrieved from the database matches the expected rows.
        res = hw.print_grades_summary()
        self.assertEqual(res[0][0], 'Bezos, J')
        self.assertEqual(res[1][4], 'Hawking, S')
        self.assertEqual(res[2][0], 'Gates, B')


if __name__ == '__main__':
    unittest.main()
