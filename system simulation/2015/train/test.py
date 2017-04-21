import unittest
import csv
import random

from train import Train

history = []


class TestSequence(unittest.TestCase):
    pass


def test_generator(distance: float, operations: str):
    def test(self):
        train = Train(accelerator=3000, brake=-4000, distance=distance)
        print(train.control(train.ascii2list(operations), debug=False))

        history.append(train.history)

        self.assertTrue(train.is_success())

    return test


def dump_history(stop=True):
    time = 0
    distance_margin = 0.0

    for section in history:
        for x in section:
            time += 1
            print(time, distance_margin + x[1], x[2])

        if stop:  # 停車時間
            for x in range(random.randint(10, 20)):
                time += 1
                print(time, distance_margin + section[len(section) - 1][1], 0)

        distance_margin += section[len(section) - 1][1]


if __name__ == '__main__':
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)

        count = 1

        for row in reader:
            if len(row) != 3:
                continue

            test_name = 'test_%02d_%s' % (count, row[0])
            test = test_generator(float(row[1]), row[2])
            setattr(TestSequence, test_name, test)

            count += 1

    unittest.main(exit=False)
    # dump_history(stop=True)
