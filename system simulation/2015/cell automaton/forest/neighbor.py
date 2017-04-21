__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from field import Field


class Neighbor:
    def __init__(self, field: Field, x: int, y: int):
        self.__neighbor = {}

        if not field.is_correct(y, x):
            raise IndexError

        for dx, dy in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:
            cx = x + dx
            cy = y + dy

            if not field.is_correct(cy, cx):
                continue

            class_name = type(field[cy][cx]).__name__

            if class_name in self.__neighbor:
                self.__neighbor[class_name] += 1
            else:
                self.__neighbor[class_name] = 1

    def dump(self):
        for key, value in self.__neighbor.items():
            print(key, value)

    def __getattr__(self, item):
        if item in self.__neighbor:
            return self.__neighbor[item]
        else:
            return 0
