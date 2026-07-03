import unittest
from mark_convert import *

A_NUM = 96
B_NUM = 82
C_NUM = 72
D_NUM = 61
E_NUM = 37
NUM_GRADES = [A_NUM, B_NUM, C_NUM, D_NUM, E_NUM]

class TestConversionFunctions(unittest.TestCase):

    def test_convert_categorical_abcde(self):
        raw_marks = {'Math': ['A']}
        result = convert_categorical(raw_marks, is_abcde=True)
        self.assertEqual(result, {'Math': A_NUM})

    def test_convert_categorical_ohsbl(self):
        raw_marks = {'Math': ['O']}
        result = convert_categorical(raw_marks, is_abcde=False)
        self.assertEqual(result, {'Math': A_NUM})

    def test_convert_weighted_num(self):
        raw_marks = {'Math': {'Homework': {'task_weight': 70, 'task_mark': 80}}}
        result = convert_weighted_num(raw_marks)
        self.assertEqual(result, {'Math': 56})

    def test_convert_multi_cat_abcde(self):
        raw_marks = {'Math': {'A': 1, 'B': 1, 'C': 0, 'D': 1, 'E': 2}}
        result = convert_multi_cat(raw_marks, is_abcde=True)
        self.assertEqual(result, {'Math': 62.6})

    def test_convert_multi_cat_ohsbl(self):
        raw_marks = {'Math': {'O': 1, 'H': 1, 'S': 0, 'B': 1, 'L': 2}}
        result = convert_multi_cat(raw_marks, is_abcde=False)
        self.assertEqual(result, {'Math': 62.6})

    def test_convert_sa_single(self):
        raw_marks = {'Math': 'A+'}
        result = convert_sa_single(raw_marks)
        self.assertEqual(result, {'Math': A_NUM + 4})

    def test_convert_weighted_sa(self):
        raw_marks = {'Math': {'Homework': {'task_weight': 70, 'task_mark': 'A+'}}}
        result = convert_weighted_sa(raw_marks)
        self.assertEqual(result, {'Math': (A_NUM + 4) * 0.7})

if __name__ == '__main__':
    unittest.main()