__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

import sys

from field import Field
from cell import *


class Forest:
    def __init__(self, x=0, y=0):
        self.x = 0
        self.y = 0

        self.__field = None
        self.__convert_table = None

        self.reset(x, y)

    def reset(self, x: int, y: int):
        self.x = x
        self.y = y

        self.__field = Field(y, x)

    def next_generation(self):
        next_field = Field(self.y, self.x)

        for y in range(self.y):
            for x in range(self.x):
                next_field[y][x] = self.__field[y][x].get_next_generation(Neighbor(self.__field, x, y))

        self.__field = next_field

    def set_cell(self, x, y, cell: Cell):
        self.__field[y][x] = cell

    def get_cell(self, x, y) -> Cell:
        return self.__field[y][x]

    def loads(self, field: str):
        if not self.__convert_table:
            self.__convert_table = {
                str(Wood()): Wood,
                str(Bamboo()): Bamboo,
                str(Fire()): Fire,
                str(Soil()): Soil,
                str(Pool()): Pool,
                str(Road()): Road,
                str(Mountain()): Mountain
            }

        lines = [line for line in field.split('\n') if line != '']
        self.reset(len(lines[0]), len(lines))

        for y in range(self.y):
            for x in range(self.x):
                self.set_cell(x, y, self.__convert_table[lines[y][x]]())

    def dumps(self) -> str:
        result = ''
        fire = 0

        for y in range(self.y):
            for x in range(self.x):
                if str(self.get_cell(x, y)) == 'F':
                    fire += 1
                result += str(self.get_cell(x, y))
            result += '\n'

        print(fire, file=sys.stderr)

        return result
