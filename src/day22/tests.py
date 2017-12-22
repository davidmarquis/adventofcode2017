from unittest import TestCase

import math


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
RIGHT = 1
LEFT = -1
REVERSE = 2
FORWARD = 0


def carrier_part1(map):
    directions = {'#': RIGHT, None: LEFT}
    states = {'#': None, None: '#'}

    return VirusCarrier(map, directions, states)


def carrier_part2(map):
    directions = {'W': FORWARD, '#': RIGHT, 'F': REVERSE, None: LEFT}
    states = {None: 'W', 'W': '#', '#': 'F', 'F': None}

    return VirusCarrier(map, directions, states)


class VirusCarrier:
    def __init__(self, map, directions_mapping, states_mapping):
        self.directions_mapping = directions_mapping
        self.states_mapping = states_mapping
        self.infections = {position: '#' for position in self.parse_infected_positions(map)}
        self.current_position = (0, 0)
        self.direction = 0
        self.num_infected = 0

    def burst(self, count=1):
        for _ in range(count):
            state = self.infections.get(self.current_position, None)
            self.direction += self.directions_mapping.get(state)

            state = self.states_mapping.get(state)
            if state is None:
                del self.infections[self.current_position]
            else:
                self.infections[self.current_position] = state
                if state == '#':
                    self.num_infected += 1

            self.current_position = translate(self.current_position, self.direction)

    @staticmethod
    def parse_infected_positions(map):
        infections = set()
        center_y = int(len(map) / 2)

        for y, row in enumerate(map):
            row = row.strip()
            center_x = int(math.floor(len(row) / 2))
            for x, char in enumerate(row):
                if char == '#':
                    position = (-(y-center_y), (x-center_x))
                    infections.add(position)
        return infections


def translate(position, direction):
    a = position
    b = DIRECTIONS[direction % len(DIRECTIONS)]
    return a[0] + b[0], a[1] + b[1]


class TestSporificaVirus(TestCase):
    def test_example_part1(self):
        map = [
            '..#',
            '#..',
            '...',
        ]

        carrier = self._run(carrier_part1, map, 7)
        self.assertEqual(5, carrier.num_infected)
        carrier = self._run(carrier_part1, map, 70)
        self.assertEqual(41, carrier.num_infected)
        carrier = self._run(carrier_part1, map, 10000)
        self.assertEqual(5587, carrier.num_infected)

    def test_example_part2(self):
        map = [
            '..#',
            '#..',
            '...',
        ]

        carrier = self._run(carrier_part2, map, 100)
        self.assertEqual(26, carrier.num_infected)

        carrier = self._run(carrier_part2, map, 10000000)
        self.assertEqual(2511944, carrier.num_infected)

    def test_solution_part1(self):
        with open('map.txt', 'r') as fin:
            map = fin.readlines()

        carrier = self._run(carrier_part1, map, 10000)

        print('Solution part 1: %s' % carrier.num_infected)

    def test_solution_part2(self):
        with open('map.txt', 'r') as fin:
            map = fin.readlines()

        carrier = self._run(carrier_part2, map, 10000000)

        print('Solution part 2: %s' % carrier.num_infected)

    def _run(self, factory_method, map, count):
        carrier = factory_method(map)
        carrier.burst(count)
        return carrier
