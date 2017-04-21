__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from abc import *
import random

from neighbor import Neighbor


class Cell(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_next_generation(self, neighbor: Neighbor):
        pass


class Wood(Cell):
    def __str__(self) -> str:
        return 'W'

    def get_next_generation(self, neighbor: Neighbor):
        if (neighbor.Fire >= 4 or (neighbor.Fire == 3 and random.random() <= 0.75) or
                (neighbor.Fire == 2 and random.random() <= 0.5) or (neighbor.Fire == 1 and random.random() <= 0.25)):
            return Fire()
        return self


class Bamboo(Cell):
    def __str__(self) -> str:
        return 'B'

    def get_next_generation(self, neighbor: Neighbor):
        if (neighbor.Fire >= 4 or (neighbor.Fire == 3 and random.random() <= 0.50) or
                (neighbor.Fire == 2 and random.random() <= 0.25) or (neighbor.Fire == 1 and random.random() <= 0.125)):
            return Fire()
        return self


class Fire(Cell):
    def __str__(self) -> str:
        return 'F'

    def get_next_generation(self, neighbor: Neighbor):
        if neighbor.Wood <= 3 and random.random() <= 0.5:
            return Soil()
        return self


class Soil(Cell):
    def __str__(self) -> str:
        return 'S'

    def get_next_generation(self, neighbor: Neighbor):
        if neighbor.Fire == 0 or (neighbor.Fire == 1 and random.random() <= 0.1):
            return Wood()
        return self


class Pool(Cell):
    def __str__(self) -> str:
        return 'P'

    def get_next_generation(self, neighbor: Neighbor):
        return self


class Road(Cell):
    def __str__(self) -> str:
        return 'R'

    def get_next_generation(self, neighbor: Neighbor):
        return self


class Mountain(Cell):
    def __str__(self) -> str:
        return 'M'

    def get_next_generation(self, neighbor: Neighbor):
        return self
