__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

import unittest
import random

from field import Field
from neighbor import Neighbor


class FieldTests(unittest.TestCase):
    def setUp(self):
        self.__x = random.randint(2, 128)
        self.__y = random.randint(2, 128)
        self.__field = Field(self.__y, self.__x)

    def test_zero(self):
        self.assertFalse(Field(0, 0).is_correct(0, 0))

    def test_size(self):
        self.assertEqual(self.__field.x, self.__x)
        self.assertEqual(self.__field.y, self.__y)

    def test_basic(self):
        n = random.random()
        x = random.randint(0, self.__x - 1)
        y = random.randint(0, self.__y - 1)
        self.__field[y][x] = n

        self.assertEqual(self.__field[y][x], n)

    def test_border(self):
        self.__field[0][0] = 0
        self.__field[self.__y - 1][self.__x - 1] = 0

    def test_method_is_correct(self):
        x = random.randint(0, self.__x - 1)
        y = random.randint(0, self.__y - 1)

        self.assertTrue(self.__field.is_correct(0, 0))
        self.assertTrue(self.__field.is_correct(y, x))
        self.assertTrue(not self.__field.is_correct(-1, 0))
        self.assertTrue(not self.__field.is_correct(0, -1))
        self.assertTrue(not self.__field.is_correct(self.__y, 0))
        self.assertTrue(not self.__field.is_correct(0, self.__x))


class NeighborTests(unittest.TestCase):
    def test_basic(self):
        field = Field(3, 3)

        self.assertEqual(Neighbor(field, 0, 0).NoneType, 3)
        self.assertEqual(Neighbor(field, 1, 0).NoneType, 5)
        self.assertEqual(Neighbor(field, 2, 0).NoneType, 3)
        self.assertEqual(Neighbor(field, 0, 1).NoneType, 5)
        self.assertEqual(Neighbor(field, 1, 1).NoneType, 8)
        self.assertEqual(Neighbor(field, 2, 1).NoneType, 5)
        self.assertEqual(Neighbor(field, 0, 2).NoneType, 3)
        self.assertEqual(Neighbor(field, 1, 2).NoneType, 5)
        self.assertEqual(Neighbor(field, 2, 2).NoneType, 3)

    def test_basic_real(self):
        class TestClassA:
            pass

        class TestClassB:
            pass

        field = Field(1, 3)
        field[0][0] = TestClassA()
        field[0][1] = TestClassB()
        field[0][2] = TestClassA()

        self.assertEqual(Neighbor(field, 0, 0).TestClassB, 1)
        self.assertEqual(Neighbor(field, 1, 0).TestClassA, 2)
        self.assertEqual(Neighbor(field, 2, 0).TestClassB, 1)

    def test_zero(self):
        field = Field(1, 1)

        self.assertEqual(Neighbor(field, 0, 0).AlwaysZero, 0)


if __name__ == '__main__':
    unittest.main()
