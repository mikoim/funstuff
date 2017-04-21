__author__ = 'Eshin Kunishima'
__license__ = 'MIT'


class Field:
    def __init__(self, y: int, x: int, initialize=None):
        self.x = x
        self.y = y
        self._field = [[initialize for i in range(x)] for j in range(y)]

    def is_correct(self, y, x) -> bool:
        return not (0 > x or 0 > y or x >= self.x or y >= self.y)

    def dump(self):
        print(*self._field, sep='\n')

    def __getitem__(self, item):
        return self._field[item]
