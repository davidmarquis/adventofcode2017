import operator
from unittest import TestCase


def reallocate_memory(banks):
    seen = set()
    banks_count = len(banks)
    rounds = 0

    while True:
        snapshot = tuple(banks)
        if snapshot in seen:
            return rounds, banks
        seen.add(snapshot)

        max_index, blocks = max(enumerate(banks), key=operator.itemgetter(1))
        banks[max_index] = 0
        for offset in range(1, blocks + 1):
            slot = (max_index + offset) % banks_count
            banks[slot] += 1
        rounds += 1


class TestMemoryReallocation(TestCase):
    def test_reallocate_memory(self):
        self.assertEqual((5, [2, 4, 1, 2]), reallocate_memory([0, 2, 7, 0]))

        rounds, match = reallocate_memory([0, 5, 10, 0, 11, 14, 13, 4, 11, 8, 8, 7, 1, 4, 12, 11])

        print('Solution part 1: %s' % rounds)
        print('Solution part 2: %s' % reallocate_memory(match)[0])