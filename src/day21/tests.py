from unittest import TestCase

import math


def make_rules(lines):
    rules = {}
    for line in lines:
        match, replacement = line.rstrip().split(' => ')
        match = to_matrix(match)
        replacement = to_matrix(replacement)
        for variation in variations_of(match):
            rules[variation] = replacement
    return rules


def to_matrix(short):
    return tuple(tuple(row) for row in short.split('/'))


def variations_of(matrix):
    yield matrix
    yield flip_horizontal(matrix)
    yield flip_vertical(matrix)

    result = matrix
    for _ in range(3):
        result = rotate90(result)
        yield result
        yield flip_horizontal(result)
        yield flip_vertical(result)


def identity(matrix):
    return matrix


def rotate90(matrix):
    return tuple(zip(*reversed(matrix)))


def flip_vertical(matrix):
    return tuple(reversed(matrix))


def flip_horizontal(matrix):
    return tuple(tuple(reversed(row)) for row in matrix)


def enhance(matrix, rules):
    sub_squares = [rules[square] for square in divide_squares(matrix)]

    merged = []
    new_grid_size = int(math.sqrt(len(sub_squares)))
    for idx in range(0, len(sub_squares), new_grid_size):
        row = collate(sub_squares[idx:idx + new_grid_size])
        merged += row
    return tuple(merged)


def divide_squares(matrix):
    if len(matrix) % 2 == 0:
        return subsquares_of(matrix, 2)
    if len(matrix) % 3 == 0:
        return subsquares_of(matrix, 3)
    

def subsquares_of(matrix, size):
    for y in range(0, len(matrix), size):
        for x in range(0, len(matrix), size):
            yield tuple(tuple(row[x:x+size]) for row in matrix[y:y+size])


def collate(matrices):
    result = [row for row in matrices[0]]
    for idx in range(1, len(matrices)):
        current = matrices[idx]
        for row_idx, row in enumerate(current):
            result[row_idx] += row
    return tuple(result)


class TestFractalArt(TestCase):
    def test_rotate90_size2(self):
        matrix = (
            ('#', '.'),
            ('.', '.'),
        )

        matrix = rotate90(matrix)
        self.assertEqual((
            ('.', '#'),
            ('.', '.'),
        ), matrix)

        matrix = rotate90(matrix)
        self.assertEqual((
            ('.', '.'),
            ('.', '#'),
        ), matrix)

    def test_rotate90_size3(self):
        matrix = (
            ('#', '.', '.'),
            ('.', '.', '.'),
            ('.', '.', '.'),
        )

        matrix = rotate90(matrix)
        self.assertEqual((
            ('.', '.', '#'),
            ('.', '.', '.'),
            ('.', '.', '.'),
        ), matrix)

        matrix = rotate90(matrix)
        self.assertEqual((
            ('.', '.', '.'),
            ('.', '.', '.'),
            ('.', '.', '#'),
        ), matrix)

    def test_flip_vertical(self):
        matrix = (
            ('#', '.', '.'),
            ('.', '.', '#'),
            ('.', '#', '.'),
        )

        matrix = flip_vertical(matrix)
        self.assertEqual((
            ('.', '#', '.'),
            ('.', '.', '#'),
            ('#', '.', '.'),
        ), matrix)

    def test_flip_horizontal(self):
        matrix = (
            ('#', '.', '.'),
            ('.', '.', '#'),
            ('.', '#', '.'),
        )

        matrix = flip_horizontal(matrix)
        self.assertEqual((
            ('.', '.', '#'),
            ('#', '.', '.'),
            ('.', '#', '.'),
        ), matrix)

    def test_rule_parsing(self):
        rules = make_rules([
            '../.# => ##./#../...',
            '.#./..#/### => #..#/..../..../#..#'
        ])

        self.assertEqual(12, len(rules))

    def test_simple_example(self):
        rules = make_rules([
            '../.# => ##./#../...',
            '.#./..#/### => #..#/..../..../#..#'
        ])
        matrix = to_matrix('.#./..#/###')

        for _ in range(2):
            matrix = enhance(matrix, rules)

    def test_solution_part1(self):
        with open('rules.txt', 'r') as fin:
            rules = make_rules(fin.readlines())
        matrix = to_matrix('.#./..#/###')

        for _ in range(5):
            matrix = enhance(matrix, rules)

        print('Solution part 1: %s' % len([cell for row in matrix for cell in row if cell == '#']))

    def test_solution_part2(self):
        with open('rules.txt', 'r') as fin:
            rules = make_rules(fin.readlines())
        matrix = to_matrix('.#./..#/###')

        for _ in range(18):
            matrix = enhance(matrix, rules)

        print('Solution part 2: %s' % len([cell for row in matrix for cell in row if cell == '#']))