__author__ = 'Eshin Kunishima'
__license__ = 'MIT'


class Field:
    def __init__(self, y: int, x: int):
        self.x = x
        self.y = y
        self.__field = [[None for i in range(x)] for j in range(y)]

    def is_correct(self, y, x) -> bool:
        return not (0 > x or 0 > y or x >= self.x or y >= self.y)

    def dump(self):
        print(*self.__field, sep='\n')

    def __getitem__(self, item):
        return self.__field[item]
