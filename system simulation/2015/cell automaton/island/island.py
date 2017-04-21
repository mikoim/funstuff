__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from enum import Enum
from copy import deepcopy
from random import randint, random

from field import Field
from neighbor import Neighbor


def clamp(num, min_num, max_num):
    return max(min(max_num, num), min_num)


class Season(Enum):
    spring = 0
    summer = 1
    autumn = 2
    winter = 3


class Cell:
    def __init__(self, grass: int, herbivore: int, carnivore: int):
        self._grass = 0
        self._herbivore = 0
        self._carnivore = 0

        self.set_grass(grass)
        self.set_herbivore(herbivore)
        self.set_carnivore(carnivore)

    def get_grass(self):
        return self._grass

    def get_herbivore(self):
        return self._herbivore

    def get_carnivore(self):
        return self._carnivore

    def set_grass(self, grass: int):
        assert 0 <= grass <= 6, '0 <= grass <= 6'
        self._grass = grass

    def set_herbivore(self, herbivore):
        assert 0 <= herbivore <= 3, '0 <= herbivore <= 3'
        self._herbivore = herbivore

    def set_carnivore(self, carnivore):
        assert 0 <= carnivore <= 1, '0 <= carnivore <= 1'
        self._carnivore = carnivore

    def get_next_generation(self, neighbor: Neighbor, season: Season):
        next_grass = self._grass
        next_herbivore = self._herbivore
        next_carnivore = self._carnivore

        if season == Season.spring:
            next_grass += 1
            next_grass -= self._herbivore
        elif season == Season.summer:
            next_grass += 2
            next_grass -= self._herbivore
        elif season == Season.autumn:
            next_grass += 1
            next_grass -= self._herbivore
        elif season == Season.winter:
            next_grass -= self._herbivore

        if self._herbivore <= self._grass and 6 <= neighbor.herbivore <= 12:
            next_herbivore += 1
        elif self._herbivore <= self._grass and 13 <= neighbor.herbivore <= 20 and (1 - ((neighbor.herbivore - 12) / 8)) <= random():
            next_herbivore += 1
        else:
            next_herbivore -= 1

        if neighbor.carnivore == 2 and neighbor.herbivore >= 6:
            next_carnivore += 1
        else:
            next_carnivore -= 1

        return Cell(clamp(next_grass, 0, 6), clamp(next_herbivore, 0, 3), clamp(next_carnivore, 0, 1))


class Island:
    def __init__(self, x=15, y=15, grass=1000, herbivore=400, carnivore=0):
        assert x > 0, 'x > 0'
        assert y > 0, 'y > 0'

        self._x = x
        self._y = y

        self._time = 0
        self._statistics = []
        self._field = Field(y, x)

        cells = []

        total_grass = 0
        total_herbivore = 0
        total_carnivore = 0

        for i in range(self._x * self._y):
            cur_grass = randint(0, 6)
            cur_herbivore = randint(0, 3)
            cur_carnivore = 0

            cells.append(Cell(cur_grass, cur_herbivore, cur_carnivore))

            total_grass += cur_grass
            total_herbivore += cur_herbivore
            total_carnivore += cur_carnivore

        print('Planting grasses...')

        while total_grass != grass:
            cell = cells[randint(0, len(cells) - 1)]

            old_grass = cell.get_grass()
            if total_grass > grass:
                new_grass = randint(0, 3)
            else:
                new_grass = randint(3, 6)

            total_grass -= old_grass
            total_grass += new_grass

            cell.set_grass(new_grass)

        print('Creating herbivores...')

        while total_herbivore != herbivore:
            cell = cells[randint(0, len(cells) - 1)]

            old_herbivore = cell.get_herbivore()
            if total_herbivore > herbivore:
                new_herbivore = randint(0, 1)
            else:
                new_herbivore = randint(2, 3)

            total_herbivore -= old_herbivore
            total_herbivore += new_herbivore

            cell.set_herbivore(new_herbivore)

        print('Creating carnivore...')

        while total_carnivore != carnivore:
            cell = cells[randint(0, len(cells) - 1)]

            old_carnivore = cell.get_carnivore()
            if total_carnivore > carnivore:
                new_carnivore = 0
            else:
                new_carnivore = 1

            total_carnivore -= old_carnivore
            total_carnivore += new_carnivore

            cell.set_carnivore(new_carnivore)

        for y in range(self._y):
            for x in range(self._x):
                self._field[y][x] = cells.pop()

        self._append_statistics()

    def _append_statistics(self, append=True):
        grass = 0
        herbivore = 0
        carnivore = 0

        for y in range(self._y):
            for x in range(self._x):
                cell = self._field[y][x]

                grass += cell.get_grass()
                herbivore += cell.get_herbivore()
                carnivore += cell.get_carnivore()

        result = (self._time, grass, herbivore, carnivore)

        if append:
            self._statistics.append(result)

        return result

    def compute_next_generation(self) ->tuple:
        next_field = deepcopy(self._field)

        for y in range(self._y):
            for x in range(self._x):
                next_field[y][x] = self._field[y][x].get_next_generation(
                    Neighbor(self._field, x, y),
                    Season(self._time % 4)
                )

        self._field = next_field

        self._time += 1

        return self._append_statistics()

    def get_time(self):
        return self._time

    def get_statistics(self):
        return self._statistics

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_cell(self, x, y, cell: Cell):
        self._field[y][x] = cell

    def get_cell(self, x, y) -> Cell:
        return self._field[y][x]


if __name__ == '__main__':
    stat = []

    for t in range(4 * 50 + 1):
        stat.append((t, 0, 0, 0))

    for l in range(10):
        print(l)

        island = Island()

        for t in range(4 * 50):
            island.compute_next_generation()

        count = 0

        for t, g, h, c in island.get_statistics():
            n = stat[count]

            stat[count] = (t, n[1] + g, n[2] + h, n[3] + c)

            count += 1

    for t, g, h, c in stat:
        print(t, g / 10, h / 10, c / 10)
