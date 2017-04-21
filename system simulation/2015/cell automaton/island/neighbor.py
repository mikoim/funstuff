__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from field import Field


class Neighbor:
    def __init__(self, field: Field, x: int, y: int):
        self._neighbor = {'grass': 0, 'herbivore': 0, 'carnivore': 0}

        if not field.is_correct(y, x):
            raise IndexError

        for dx, dy in [(0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:
            cx = x + dx
            cy = y + dy

            if not field.is_correct(cy, cx):
                continue

            self._neighbor['grass'] += field[cy][cx].get_grass()
            self._neighbor['herbivore'] += field[cy][cx].get_herbivore()
            self._neighbor['carnivore'] += field[cy][cx].get_carnivore()

    def dump(self):
        for key, value in self._neighbor.items():
            print(key, value)

    def __getattr__(self, item):
        if item in self._neighbor:
            return self._neighbor[item]
        else:
            return 0
