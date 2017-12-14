from functools import reduce
from unittest import TestCase


def part1(num_elements, lengths):
    elements = hash_sparse(num_elements, lengths, 1)
    return elements[0] * elements[1]


def part2_knot_hash(input):
    sparse_hash = hash_sparse(256, input, 64)
    dense_hash = map(lambda block: xor_block(sparse_hash, block), range(0, 16))
    return reduce(lambda hexa, num: hexa + '{:02x}'.format(num), dense_hash, '')


def knot_hash(input_str):
    input = [ord(char) for char in input_str]
    input += [17, 31, 73, 47, 23]
    return part2_knot_hash(input)


def hash_sparse(num_elements, lengths, rounds):
    elements = list(range(0, num_elements))

    current_position = 0
    skip_size = 0
    for _ in range(0, rounds):
        for length in lengths:
            block = list(cycle_slice(elements, current_position, length))
            block.reverse()
            replace_items(elements, current_position, block)

            current_position += (length + skip_size) % len(elements)
            skip_size += 1

    return elements


def cycle_slice(items, start, length):
    for idx in range(start, start + length):
        yield items[idx % len(items)]


def replace_items(destination, start_position, replacements):
    for idx, value in enumerate(replacements):
        destination[(start_position + idx) % len(destination)] = replacements[idx]


def xor_block(sparse_hash, block):
    block_start = 16 * block
    return reduce(lambda x, y: x ^ y, sparse_hash[block_start:block_start+16])


class TestKnotHash(TestCase):
    def test_part1(self):
        self.assertEqual(12, part1(5, [3, 4, 1, 5]))
        
        print('Solution part 1: %s' % part1(256, [183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88]))

    def test_part2(self):
        print('Solution part 2: %s' % knot_hash('183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88'))
