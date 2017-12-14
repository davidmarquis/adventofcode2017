from unittest import TestCase

from day10.tests import knot_hash


GRID_SIZE = 128


def count_squares(input):
    return sum([sum(row) for row in build_disk_grid(input)])


def count_regions(input):
    sweeper = GridSweeper(build_disk_grid(input), GRID_SIZE, GRID_SIZE)

    discovered_regions = 0
    for y in range(0, GRID_SIZE):
        for x in range(0, GRID_SIZE):
            if sweeper.sweep_region_from(x, y):
                discovered_regions += 1

    return discovered_regions


def build_disk_grid(input):
    hashes = map(lambda idx: knot_hash(input + '-' + str(idx)), range(0, GRID_SIZE))
    rows = map(lambda hash: [int(ch) for ch in str(bin(int(hash, 16)))[2:].zfill(GRID_SIZE)], hashes)
    return list(rows)


class GridSweeper:
    def __init__(self, rows, width, height):
        self.rows = rows
        self.width = width
        self.height = height
        self.sweep_states = [[0 for x in range(self.width)] for y in range(self.height)]

    def has_value(self, x, y):
        return self.rows[y][x]

    def is_swept(self, x, y):
        return self.sweep_states[y][x] == 1

    def sweep_cell(self, x, y):
        self.sweep_states[y][x] = 1

    def sweep_region_from(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        if self.is_swept(x, y):
            return False

        cell = self.has_value(x, y)
        self.sweep_cell(x, y)
        if cell:
            self.sweep_region_from(x, y + 1)
            self.sweep_region_from(x, y - 1)
            self.sweep_region_from(x + 1, y)
            self.sweep_region_from(x - 1, y)
            return True
        else:
            return False


class TestDiskDefragmentation(TestCase):
    def test_example(self):
        self.assertEqual(8108, count_squares('flqrgnkx'))
        self.assertEqual(1242, count_regions('flqrgnkx'))

    def test_solution(self):
        print('Solution part 1: %s' % count_squares('ffayrhll'))
        print('Solution part 2: %s' % count_regions('ffayrhll'))