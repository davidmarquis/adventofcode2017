from unittest import TestCase


alphabet = 'abcdefghijklmnopqrstuvwxyz'
letter_identities = {letter: 1 << idx for idx, letter in enumerate(alphabet)}


def count_valid_passphrases(input, word_hash_func=hash):
    return len([passphrase for passphrase in input if is_valid(passphrase, word_hash_func)])


def is_valid(passphrase, word_hash_func):
    words = passphrase.split()
    return len(set([word_hash_func(word) for word in words])) == len(words)


def anagram_insensitive_hash(word):
    return sum([letter_identities[letter] for letter in word])


class TestPassphrases(TestCase):
    def test_part1(self):
        self.assertEqual(1, count_valid_passphrases(['aa bb cc dd ee']))
        self.assertEqual(0, count_valid_passphrases(['aa bb cc dd aa']))
        self.assertEqual(1, count_valid_passphrases(['aa bb cc dd aaa']))

        with open('passphrases.txt', 'r') as fin:
            print('Solution part 1: %s' % count_valid_passphrases(fin.readlines()))

    def test_part2(self):
        self.assertEqual(1, count_valid_passphrases(['abcde fghij'], anagram_insensitive_hash))
        self.assertEqual(0, count_valid_passphrases(['abcde xyz ecdab'], anagram_insensitive_hash))
        self.assertEqual(1, count_valid_passphrases(['a ab abc abd abf abj'], anagram_insensitive_hash))
        self.assertEqual(0, count_valid_passphrases(['oiii ioii iioi iiio'], anagram_insensitive_hash))

        with open('passphrases.txt', 'r') as fin:
            print('Solution part 2: %s' % count_valid_passphrases(fin.readlines(), anagram_insensitive_hash))