import unittest
import random
from string import ascii_letters

import wordle

class WordleTestCase(unittest.TestCase):

  @classmethod
  def setUp(cls):
    cls.corpus = corpus = {'bbccc', 'abddd', 'defff', 'abcde', 'ghiii', 'dgggg'}
    cls.candidates = corpus = {'great', 'glean', 'gleam', 'clean'}

  def test_include(self):
    self.assertEqual({'abddd', 'abcde'}, wordle.include('a', self.corpus))
    self.assertEqual({'abddd', 'abcde'}, wordle.include('ad', self.corpus))
    self.assertEqual(set(), wordle.include('adg', self.corpus))

  def test_exclude(self):
    self.assertEqual({'bbccc', 'defff', 'ghiii', 'dgggg'}, wordle.exclude('a', self.corpus))
    self.assertEqual({'bbccc', 'ghiii'}, wordle.exclude('ad', self.corpus))
    self.assertEqual(set(), wordle.exclude('bdg', self.corpus))

  def test_matches(self):
    self.assertTrue(random.choice(ascii_letters), wordle.matches('.'))
    self.assertTrue('abc', wordle.matches('...'))
    self.assertTrue('abc', wordle.matches('a..'))
    self.assertTrue('abc', wordle.matches('.b.'))
    self.assertTrue('abc', wordle.matches('..c'))
    self.assertTrue('abc', wordle.matches('ab.'))
    self.assertTrue('abc', wordle.matches('a.c'))
    self.assertTrue('abc', wordle.matches('.bc'))
    self.assertTrue('abc', wordle.matches('abc'))

  def test_search(self):
    self.assertEqual({'bbccc', 'abddd', 'abcde'}, wordle.search('.b...', self.corpus))
    self.assertEqual({'bbccc', 'abcde'}, wordle.search('.bc..', self.corpus))
    self.assertEqual({'abddd', 'abcde'}, wordle.search('.b.d.', self.corpus))
    self.assertEqual(set(), wordle.search('.bz..', self.corpus))
    self.assertEqual(self.corpus, wordle.search('.....', self.corpus))

  def test_union(self):
    self.assertEqual(set(), wordle.union([]))
    self.assertEqual({'a', 'b'}, wordle.union([{'a'}, {'b'}]))
    self.assertEqual({'a', 'b'}, wordle.union([{'a'}, {'b'}, {'a', 'b'}]))
    self.assertEqual({'a', 'b', 'c'}, wordle.union([{'a'}, {'b'}, {'a', 'b'}, {'a', 'c'}, {'b', 'c'}]))

  def test_discard(self):
    self.assertEqual(set(), wordle.discard(['.....'], self.corpus))
    self.assertEqual({'defff', 'ghiii', 'dgggg'}, wordle.discard(['.b...'], self.corpus))
    self.assertEqual({'defff', 'dgggg'}, wordle.discard(['.b...', '...i.'], self.corpus))
    self.assertEqual({'dgggg'}, wordle.discard(['.b...', '...i.', '..f..'], self.corpus))
    self.assertEqual(set(), wordle.discard(['.b...', '...i.', 'd....'], self.corpus))

  def test_tabulate(self):
    expected = {
      0: {'c': 0.25, 'g': 0.75},
      1: {'l': 0.75, 'r': 0.25},
      2: {'e': 1.0},
      3: {'a': 1.0},
      4: {'m': 0.25, 'n': 0.5, 't': 0.25}}

    self.assertEqual(expected, wordle.tabulate(self.candidates))

  def test_score(self):
    expected = [
      wordle.WordScore(word='glean', score=0.28125),
      wordle.WordScore(word='gleam', score=0.140625),
      wordle.WordScore(word='clean', score=0.09375),
      wordle.WordScore(word='great', score=0.046875)]

    self.assertEqual(expected, wordle.score(self.candidates))
