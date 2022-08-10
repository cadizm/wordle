import sys
import re
from functools import reduce
from collections import defaultdict


"""
TODO
  1. Tests
  2. Based on previous guess, suggest next guess (e.g., after using "ea"
     vowels on first try, suggest words with "ous", etc
  3. Productionize as webapp on cadizm.com
  4. Comments and blog post with complexity analysis
"""


def read_corpus(infile):
  """
  Read infile (dictionary with 1 word per line) and return its contents as a set.
  """
  return set(map(lambda line: line.strip(), open(infile).readlines()))


def include(letters, corpus):
  """
  Return words in corpus that include all letters in `letters`.
  """
  return set(filter(lambda word: set(word) & set(letters) == set(letters), corpus))


def exclude(letters, corpus):
  """
  Return words in corpus that exclude all letters in `letters`.
  """
  return set(filter(lambda word: set(word) & set(letters) == set(), corpus))


def matches(regex):
  """
  Return lambda returning True when its argument matches `regex1`.
  """
  return lambda x: re.fullmatch(regex, x)


def search(wordle, corpus):
  """
  Search words in corpus matching the regular expression specified in `wordle`.
  """
  return set(filter(matches(wordle), corpus))


def union(sets):
  """
  Return the union of the list of sets in `sets`.
  """
  return reduce(lambda x, y: x.union(y), sets)


def discard(misplaced, corpus):
  """
  Discard from corpus words matching regular expressions in list `misplaced`.
  """
  return set(corpus) - union(map(lambda wordle: search(wordle, corpus), misplaced))


def letter_score(index, candidates):
  n = len(candidates)

  freq = defaultdict(int)
  for word in candidates:
    letter = word[index]
    freq[letter] += 1

  table = defaultdict(dict)
  for letter in freq:
    table[index][letter] = freq[letter] / n

  return table


def word_score(word, table):
  score = 1
  for index, letter in enumerate(word):
    score *= table[index][letter]

  return (score, word)


def score(candidates):
  wordle_len = 5
  table = {}
  for index in range(wordle_len):
    table.update(letter_score(index, candidates))

  scores = []
  for word in candidates:
    scores.append(word_score(word, table))

  return sorted(scores, key=lambda x: x[0], reverse=True)


if __name__ == '__main__':
  infile = './5-letter-words.txt'
  if len(sys.argv) > 1:
    infile = sys.argv[1]

  wordle = '..t..'
  excluded = 'greuos'
  included = 'at'
  misplaced = ['...a.', '....t', 'a....']

  candidates = sorted(discard(misplaced, search(wordle, exclude(excluded, include(included, read_corpus(infile))))))

  for score, word in score(candidates):
    print(f'{score:.7f} {word}')
