from unittest import TestCase


class Firewall:
    def __init__(self):
        self.ranges = []

    def add_layer(self, depth, scanner_range):
        self.ranges.append((depth, scanner_range))

    def analyze_packet(self, delay=0):
        return sum(self.pass_through(delay))

    def pass_through(self, delay):
        for depth, scanner_range in self.ranges:
            scanner_position = (depth + delay) % (2 * (scanner_range - 1))
            if scanner_position == 0:
                yield scanner_range * depth

    @staticmethod
    def of(lines):
        fw = Firewall()
        for line in lines:
            info = line.split(': ')
            fw.add_layer(int(info[0]), int(info[1]))
        return fw


class TestPacketScanners(TestCase):
    def test_example(self):
        lines = [
            '0: 3',
            '1: 2',
            '4: 4',
            '6: 4',
        ]

        fw = Firewall.of(lines)

        self.assertEqual(24, fw.analyze_packet())
        self.assertEqual(0, fw.analyze_packet(10))
        with self.assertRaises(StopIteration):
            next(fw.pass_through(10))

    def test_solution(self):
        with open('layers.txt', 'r') as fin:
            fw = Firewall.of(fin.readlines())

            print('Solution part 1: %s' % fw.analyze_packet())

            delay = 0
            try:
                while True:
                    delay += 1
                    next(fw.pass_through(delay))
            except StopIteration:
                pass

            print('Solution part 2: %s' % delay)
