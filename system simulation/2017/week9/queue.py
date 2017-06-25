import itertools
import json
import random
import statistics


def arrival_static(time_line: list, time_slice: int, customer_per_slice: int):
    for i in range(time_slice, len(time_line), time_slice):
        time_line[i] += customer_per_slice


def arrival_random(time_line: list, time_slice: int, customer_per_slice: int):
    full_fill_count = len(time_line) // time_slice
    for n in range(full_fill_count):
        for _ in range(customer_per_slice):
            a = n * time_slice
            b = (n + 1) * time_slice - 1
            time_line[random.randint(a, b)] += 1

    part_fill_diff = len(time_line) - full_fill_count * time_slice
    if part_fill_diff is not 0:
        for _ in range(customer_per_slice):
            a = len(time_line) - part_fill_diff
            b = a + time_slice

            r = random.randint(a, b)
            if r <= len(time_line) - 1:
                time_line[r] += 1


def sim(customer_per_slice=6, time_slice=600, duration=17 * 60, max_seat=9, arrival_function=arrival_random):
    # variables
    time_line = [0] * 3600
    queue = []
    seat = []
    leaver = 0
    result = []

    # step 1
    arrival_function(time_line, time_slice, customer_per_slice)

    # step 2
    t = 0
    while True:
        if t >= len(time_line) and len(queue) == 0 and len(seat) == 0:
            break

        # simulate eating
        seat = list(map(lambda x: x - 1, seat))
        before_seat_count = len(seat)
        seat = [x for x in seat if x != 0]
        leaver += before_seat_count - len(seat)

        # waiting time
        queue = list(map(lambda x: x + 1, queue))

        # de-queue
        for _ in range(max_seat - len(seat)):
            if len(queue) == 0:
                break

            queue.pop()
            seat.append(duration)

        # en-queue
        if t < len(time_line):
            for _ in range(time_line[t]):
                queue.append(0)

        # check queue length
        result.append(len(queue))

        t += 1

    return result


if __name__ == '__main__':
    # Problem 1 random
    # for n in range(2, 11, 1):
    #     l = [sim(n) for _ in range(10000)]
    #
    #     max_queue_len = max(map(max, l))
    #     min_queue_len = min(map(min, l))
    #     mean_queue_len = statistics.mean(map(statistics.mean, l))
    #
    #     max_closed_time = max(map(len, l))
    #     min_closed_time = min(map(len, l))
    #     mean_closed_time = statistics.mean(map(len, l))
    #
    #     mean_queue_list = list(map(statistics.mean, itertools.zip_longest(*l, fillvalue=0)))
    #
    #     print(n, max_queue_len, mean_queue_len, min_queue_len, max_closed_time, mean_closed_time, min_closed_time)
    #
    #     with open('random/{:d}.json'.format(n), mode='w') as fp:
    #         json.dump(mean_queue_list, fp)

    # Problem 2
    # for consumer, duration, seat in itertools.product(range(8, 11, 2), range(2 * 60, 21 * 60, 120), range(2, 11, 2)):
    #     l = [sim(consumer, duration=duration, max_seat=seat) for _ in range(1000)]
    #
    #     max_queue_len = max(map(max, l))
    #     min_queue_len = min(map(min, l))
    #     mean_queue_len = statistics.mean(map(statistics.mean, l))
    #
    #     max_closed_time = max(map(len, l))
    #     min_closed_time = min(map(len, l))
    #     mean_closed_time = statistics.mean(map(len, l))
    #
    #     print(consumer, duration, seat, max_queue_len, mean_queue_len, min_queue_len, max_closed_time, mean_closed_time, min_closed_time)

    # Problem 1 static
    # for n in range(2, 11, 1):
    #     l = [sim(1, time_slice=600 // n, arrival_function=arrival_static) for _ in range(1)]
    #
    #     max_queue_len = max(map(max, l))
    #     min_queue_len = min(map(min, l))
    #     mean_queue_len = statistics.mean(map(statistics.mean, l))
    #
    #     max_closed_time = max(map(len, l))
    #     min_closed_time = min(map(len, l))
    #     mean_closed_time = statistics.mean(map(len, l))
    #
    #     mean_queue_list = list(map(statistics.mean, itertools.zip_longest(*l, fillvalue=0)))
    #
    #     print(n, max_queue_len, mean_queue_len, min_queue_len, max_closed_time, mean_closed_time, min_closed_time)
    #
    #     with open('static/{:d}.json'.format(n), mode='w') as fp:
    #         json.dump(mean_queue_list, fp)
