import unittest
import random
from string import ascii_letters

import wordle

class WordleTestCase(unittest.TestCase):

  @classmethod
  def setUp(cls):
    cls.lexicon = lexicon = {'bbccc', 'abddd', 'defff', 'abcde', 'ghiii', 'dgggg'}
    cls.candidates = lexicon = {'great', 'glean', 'gleam', 'clean'}

  def test_include(self):
    self.assertEqual({'abddd', 'abcde'}, wordle.include('a', self.lexicon))
    self.assertEqual({'abddd', 'abcde'}, wordle.include('ad', self.lexicon))
    self.assertEqual(set(), wordle.include('adg', self.lexicon))

  def test_exclude(self):
    self.assertEqual({'bbccc', 'defff', 'ghiii', 'dgggg'}, wordle.exclude('a', self.lexicon))
    self.assertEqual({'bbccc', 'ghiii'}, wordle.exclude('ad', self.lexicon))
    self.assertEqual(set(), wordle.exclude('bdg', self.lexicon))

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
    self.assertEqual({'bbccc', 'abddd', 'abcde'}, wordle.search('.b...', self.lexicon))
    self.assertEqual({'bbccc', 'abcde'}, wordle.search('.bc..', self.lexicon))
    self.assertEqual({'abddd', 'abcde'}, wordle.search('.b.d.', self.lexicon))
    self.assertEqual(set(), wordle.search('.bz..', self.lexicon))
    self.assertEqual(self.lexicon, wordle.search('.....', self.lexicon))

  def test_union(self):
    self.assertEqual(set(), wordle.union([]))
    self.assertEqual({'a', 'b'}, wordle.union([{'a'}, {'b'}]))
    self.assertEqual({'a', 'b'}, wordle.union([{'a'}, {'b'}, {'a', 'b'}]))
    self.assertEqual({'a', 'b', 'c'}, wordle.union([{'a'}, {'b'}, {'a', 'b'}, {'a', 'c'}, {'b', 'c'}]))

  def test_discard(self):
    self.assertEqual(set(), wordle.discard(['.....'], self.lexicon))
    self.assertEqual({'defff', 'ghiii', 'dgggg'}, wordle.discard(['.b...'], self.lexicon))
    self.assertEqual({'defff', 'dgggg'}, wordle.discard(['.b...', '...i.'], self.lexicon))
    self.assertEqual({'dgggg'}, wordle.discard(['.b...', '...i.', '..f..'], self.lexicon))
    self.assertEqual(set(), wordle.discard(['.b...', '...i.', 'd....'], self.lexicon))

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

  def test_wordle_2022_09_08(self):
    expected = set(['clays', 'class', 'claps', 'claws', 'clads', 'clams'])
    actual = set(map(lambda word_score: word_score.word, wordle.suggest('cla.s', 'gretbin',['...a.', '.a...', '...l.'])))

    self.assertEqual(expected, actual)

  def test_wordle_2022_09_10(self):
    expected = set(['jolty', 'lofty', 'volti'])
    actual = set(map(lambda word_score: word_score.word, wordle.suggest('.o.t.', 'greapusmto',['....t'])))

    self.assertEqual(expected, actual)

  def test_wordle_2022_09_11(self):
    expected = set(['tabid', 'tabla', 'tabby', 'tabun', 'tibia'])
    actual = set(map(lambda word_score: word_score.word, wordle.suggest('.....', 'greos',
        ['...a.', '....t', 'b....', '..a..', '...t.'])))

    self.assertEqual(expected, actual)
