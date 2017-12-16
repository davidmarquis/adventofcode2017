from functools import reduce
from unittest import TestCase


def moves_from(text):
    return map(to_move, text.split(','))


def to_move(text):
    type = text[0]
    if type == 's':
        count = int(text[1:])
        return lambda p: spin(p, count)
    if type == 'x':
        a, b = text[1:].split('/')
        return lambda p: exchange(p, int(a), int(b))
    if type == 'p':
        a, b = text[1:].split('/')
        return lambda p: partner(p, a, b)


def dance(programs, moves):
    return ''.join(reduce(lambda p, move: move(p), moves, list(programs)))


def spin(programs, count):
    return programs[-count:] + programs[0:-count]


def exchange(programs, a, b):
    programs[b], programs[a] = programs[a], programs[b]
    return programs


def partner(programs, a, b):
    return exchange(programs, programs.index(a), programs.index(b))


class TestPermutationPromenade(TestCase):
    def test_simple_dance(self):
        programs = 'abcde'

        self.assertEqual('baedc', dance(programs, moves_from('s1,x3/4,pe/b')))

    def test_solution_part1(self):
        programs = 'abcdefghijklmnop'

        with open('moves.txt', 'r') as fin:
            print('Solution part 1: %s' % dance(programs, moves_from(fin.read())))

    def test_solution_part2(self):
        programs = 'abcdefghijklmnop'

        with open('moves.txt', 'r') as fin:
            moves = list(moves_from(fin.read()))
            past_moves = []

            for i in range(0, 100000000):
                programs = dance(programs, moves)
                if programs in past_moves:
                    # this dance repeats itself!
                    print('Solution part 2: %s' % past_moves[1000000000 % len(past_moves) - 1])
                    break
                past_moves.append(programs)
