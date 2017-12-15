from unittest import TestCase

from itertools import islice

import time


def basic_generator(initial, factor):
    value = initial
    while True:
        value = (value * factor) % 2147483647
        yield value


def picky_generator(wrapped, pick_multiples_of):
    mask = pick_multiples_of - 1
    while True:
        value = next(wrapped)
        if value & mask == 0:
            yield value


def judge(genA, genB, num_rounds):
    mask_last_16_bits = (1 << 16) - 1

    matches = 0
    for a, b in islice(zip(genA, genB), num_rounds):
        if a & mask_last_16_bits == b & mask_last_16_bits:
            matches += 1
    return matches


class TestGenerators(TestCase):
    def build_test_generators(self):
        return basic_generator(65, 16807), basic_generator(8921, 48271)

    def build_test_picky_generators(self):
        a, b = self.build_test_generators()
        return picky_generator(a, pick_multiples_of=4), picky_generator(b, pick_multiples_of=8)

    def test_basic_generator(self):
        genA, genB = self.build_test_generators()

        self.assertEqual([
            1092455,
            1181022009,
            245556042,
            1744312007,
            1352636452,
        ], list(islice(genA, 5)))

        self.assertEqual([
            430625591,
            1233683848,
            1431495498,
            137874439,
            285222916,
        ], list(islice(genB, 5)))

    def test_judge_with_basic_generators_small_sample(self):
        genA, genB = self.build_test_generators()

        self.assertEqual(1, judge(genA, genB, 5))

    def test_judge_with_basic_generators_huge_sample(self):
        genA, genB = self.build_test_generators()

        self.assertEqual(588, judge(genA, genB, 40000000))

    def test_picky_generator(self):
        genA, genB = self.build_test_picky_generators()

        self.assertEqual([
            1352636452,
            1992081072,
            530830436,
            1980017072,
            740335192,
        ], list(islice(genA, 5)))

        self.assertEqual([
            1233683848,
            862516352,
            1159784568,
            1616057672,
            412269392,
        ], list(islice(genB, 5)))

    def test_judge_with_picky_generators_huge_sample(self):
        genA, genB = self.build_test_picky_generators()

        self.assertEqual(309, judge(genA, genB, 5000000))

    def test_solution_part1(self):
        genA = basic_generator(516, 16807)
        genB = basic_generator(190, 48271)

        start = time.time()
        print('Solution part 1: %s' % judge(genA, genB, 40000000))
        print("Took {:.2f}s".format(time.time() - start))

    def test_solution_part2(self):
        genA = picky_generator(basic_generator(516, 16807), pick_multiples_of=4)
        genB = picky_generator(basic_generator(190, 48271), pick_multiples_of=8)

        start = time.time()
        print('Solution part 2: %s' % judge(genA, genB, 5000000))
        print("Took {:.2f}s".format(time.time() - start))