import operator
from unittest import TestCase


directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


class Maze:
    def __init__(self, lines):
        self.grid = build_grid(lines)

    def travel_through(self):
        letters_encountered = []
        position = (0, self.grid[0].index('|'))
        direction = 0
        moves = 0

        while True:
            moves += 1
            position = translate(position, direction)
            content = self._value_at(position)

            if content in ('-', '|'):
                continue
            elif content == ' ':
                break
            elif content == '+':
                if self._value_at(translate(position, direction + 1)) != ' ':
                    direction += 1
                elif self._value_at(translate(position, direction - 1)) != ' ':
                    direction -= 1
            else:
                letters_encountered.append(content)

        return ''.join(letters_encountered), moves

    def _value_at(self, position):
        return self.grid[position[0]][position[1]]


def build_grid(lines):
    grid = []
    width = max(len(line) for line in lines)
    for line in lines:
        line = line.rstrip()
        grid.append(list(line) + [' '] * (width-len(line)))
    return grid


def translate(position, direction):
    return tuple(map(operator.add, position, directions[direction % len(directions)]))


class TestMaze(TestCase):
    def test_simple_maze(self):
        maze = Maze([
            '     |              ',
            '     |  +--+        ',
            '     A  |  C        ',
            ' F---|----E|--+     ',
            '     |  |  |  D     ',
            '     +B-+  +--+     ',
        ])

        self.assertEqual(('ABCDEF', 38), maze.travel_through())

    def test_solutions(self):
        with open('maze.txt') as fin:
            lines = fin.readlines()
            
        print(Maze(lines).travel_through())
