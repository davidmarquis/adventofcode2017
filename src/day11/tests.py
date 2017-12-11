from unittest import TestCase


directions = {
    'nw': ( 1, -1,  0),
    'n':  ( 1,  0, -1),
    'ne': ( 0,  1, -1),
    'se': (-1,  1,  0),
    's':  (-1,  0,  1),
    'sw': ( 0, -1,  1 )
}


def distance_from_center(position):
    return (abs(position[0]) + abs(position[1]) + abs(position[2])) / 2


def all_distances(moves):
    position = (0, 0, 0)
    for move in moves:
        position = tuple(sum(t) for t in zip(position, directions[move]))
        yield distance_from_center(position)


def distance_after_moves(moves):
    distance = 0
    for distance in all_distances(moves):
        pass
    return distance


def max_observed_distance(moves):
    return max(all_distances(moves))


class TestHexEd(TestCase):
    def test_hex_grid(self):
        self.assertEqual(3, distance_after_moves(['ne', 'ne', 'ne']))
        self.assertEqual(0, distance_after_moves(['ne', 'ne', 'sw', 'sw']))
        self.assertEqual(2, distance_after_moves(['ne', 'ne', 's', 's']))

        with open('moves.txt', 'r') as fin:
            moves = fin.read().split(',')
            print('Solution part 1: %s' % distance_after_moves(moves))
            print('Solution part 2: %s' % max_observed_distance(moves))