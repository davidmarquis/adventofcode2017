import re
from unittest import TestCase


def sanitize(text):
    text = re.sub('!.', '', text)

    num_discarded = 0

    def count_and_discard(matchobj):
        nonlocal num_discarded
        num_discarded += len(matchobj.group(0)) - 2
        return ''

    text = re.sub('<(.*?)>', count_and_discard, text)

    return text, num_discarded


def score(text):
    text, _ = sanitize(text)

    depth = 0
    score = 0
    for char in text:
        if char == '{':
            depth += 1
        if char == '}':
            score += depth
            depth -= 1

    return score


class TestStreamProcessing(TestCase):
    def test_sanitize(self):
        self.assertEqual(('<', 0), sanitize('<!>'))
        self.assertEqual(('', 0), sanitize('<>'))
        self.assertEqual(('', 6), sanitize('<aihjji>'))
        self.assertEqual(('', 3), sanitize('<<<<>'))
        self.assertEqual(('', 2), sanitize('<{!>}>'))
        self.assertEqual(('', 0), sanitize('<!!>'))
        self.assertEqual(('', 0), sanitize('<!!!>>'))
        self.assertEqual(('', 10), sanitize('<{o"i!a,<{i<a>'))
        self.assertEqual(('{{}}', 13), sanitize('{{<!>},{<!>},{<!>},{<a>}}'))

    def test_score(self):
        self.assertEqual(1, score('{}'))
        self.assertEqual(6, score('{{{}}}'))
        self.assertEqual(5, score('{{},{}}'))
        self.assertEqual(16, score('{{{},{},{{}}}}'))
        self.assertEqual(1, score('{<a>,<a>,<a>,<a>}'))
        self.assertEqual(9, score('{{<ab>},{<ab>},{<ab>},{<ab>}}'))
        self.assertEqual(9, score('{{<!!>},{<!!>},{<!!>},{<!!>}}'))
        self.assertEqual(3, score('{{<a!>},{<a!>},{<a!>},{<ab>}}'))

    def test_solutions(self):
        with open('stream.txt', 'r') as fin:
            stream = fin.read()

            print('Solution part 1: %s' % score(stream))
            print('Solution part 2: %s' % sanitize(stream)[1])
