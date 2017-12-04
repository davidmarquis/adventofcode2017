import operator
from unittest import TestCase


def distance_from_center(nth_cell):
    table = SpiralTable()

    for step in range(1, nth_cell):
        table.advance()

    return sum(abs(coordinate) for coordinate in table.location)


def first_sum_of_neighbors_larger_than_input(input):
    table = SpiralTable()

    for step in range(1, input):

        def sum_neighbors():
            return sum([table.value_at(neighbor) or 0 for neighbor in table.neighboring_cells()])

        location = table.advance()
        value = table.store(location, sum_neighbors())

        if value > input:
            return value

    return None


def translate(cell, coordinates):
    return tuple(map(operator.add, cell, coordinates))


class SpiralTable:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    neighbors = [(0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self):
        self.location = (0, 0)
        self.cells = {self.location: 1}
        self.direction = 0

    def advance(self):
        direction = self.direction
        if not self.peek(direction + 1):
            direction += 1
        self.direction = direction
        self.location = self.move_towards(self.direction)
        self.store(self.location, 1)
        return self.location

    def peek(self, direction):
        return self.value_at(self.move_towards(direction))

    def value_at(self, cell):
        return self.cells.get(cell, None)

    def move_towards(self, direction):
        return translate(self.location, self.directions[direction % 4])

    def store(self, cell, value):
        self.cells[cell] = value
        return value

    def neighboring_cells(self):
        return [translate(self.location, move) for move in self.neighbors]


class TestChecksum(TestCase):
    def test_part1(self):
        self.assertEqual(0, distance_from_center(1))
        self.assertEqual(3, distance_from_center(12))
        self.assertEqual(2, distance_from_center(23))
        self.assertEqual(31, distance_from_center(1024))

        print('Solution part 1: %s' % distance_from_center(325489))

    def test_part2(self):
        self.assertEqual(10, first_sum_of_neighbors_larger_than_input(6))

        print('Solution part 2: %s' % first_sum_of_neighbors_larger_than_input(325489))
