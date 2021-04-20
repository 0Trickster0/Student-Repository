"""
This file in a unit test file for homework 9
Author: Shengping Xu
"""
import unittest
import HW09_Shengping_Xu as hw


class FileSummarizeTestCase(unittest.TestCase):
    """Test class to test the classes and functions in homework 9"""
    def test_file_summarize(self) -> None:
        """Test cases to test the classes and functions in homework 9"""
        hw.main('E:\\pyProject\\Sol\\venv\\Scripts\\810homework\\Stevens')
        self.assertEqual(hw.university.students_dic['10103'].name, 'Baldwin,C')
        self.assertEqual(hw.university.students_dic['11399'].name, 'Cordova,i')
        self.assertEqual(hw.university.instructors_dic['98761'].name, 'Edison,A')
        self.assertEqual(hw.university.instructors_dic['98763'].name, 'Newton,I')


if __name__ == '__main__':
    unittest.main()
