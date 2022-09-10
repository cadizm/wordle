import os
import sys
import re
from functools import reduce
from collections import defaultdict, namedtuple


def read_corpus(infile):
  """
  Read infile (dictionary with 1 word per line) and return its contents as a set.
  """
  return set(map(lambda line: line.strip(), open(infile).readlines()))


def exclude(letters, corpus):
  """
  Return words in corpus that exclude all letters in `letters`.
  """
  return set(filter(lambda word: set(word) & set(letters) == set(), corpus))


def matches(regex):
  """
  Return lambda returning True when its argument matches `regex`.
  """
  return lambda x: re.fullmatch(f'^{regex}$', x)


def search(wordle, corpus):
  """
  Search words in corpus matching the regular expression specified in `wordle`.
  """
  return set(filter(matches(wordle), corpus))


def union(sets):
  """
  Return the union of the list of sets in `sets`.
  """
  return reduce(lambda x, y: x.union(y), sets, set())


def discard(misplaced, corpus):
  """
  Discard from corpus words matching regular expressions in list `misplaced`.
  """
  return set(corpus) - union(map(lambda wordle: search(wordle, corpus), misplaced))


def tabulate(candidates):
  """
  Return table of letter scores in `candidates` indexed by letter position.

  For example, for a wordle length of 5 (index 0-4), a possible table of letter scores
  is shown below. We can see that at index 0, the letters `c`, `f`, `i`, and `p` all
  have scores of 0.25. At index 1, `c` and `i` have score 0.25, while `l` has score 0.5.
  Indices 2-4 can be read similarly.

    { 0: {'c': 0.25, 'f': 0.25, 'i': 0.25, 'p': 0.25},
      1: {'c': 0.25, 'i': 0.25, 'l': 0.5},
      2: {'i': 1.0},
      3: {'n': 1.0},
      4: {'g': 1.0} }
  """
  table = defaultdict(dict)
  wordle_len = max(map(lambda x: len(x), candidates), default=5)

  for index in range(wordle_len):
    freq = defaultdict(int)
    for word in candidates:
      freq[word[index]] += 1
    for letter in freq:
      table[index][letter] = freq[letter] / len(candidates)

  return table


WordScore = namedtuple('WordScore', ['word', 'score'])

def score(candidates):
  """
  Return a list of `WordScore`'s for words in `candidates` in descending score order.

  A candidate's WordScore is the product of the tabulated letter scores in the word.
  """
  scores = []
  table = tabulate(candidates)

  for word in candidates:
    score = 1
    for index, letter in enumerate(word):
      score *= table[index][letter]
    scores.append(WordScore(word, score))

  return sorted(scores, key=lambda x: x.score, reverse=True)


corpus = read_corpus(os.path.abspath(os.path.join(os.path.dirname(__file__), '5-letter-words.txt')))

def suggest(wordle, excluded, misplaced):
  """
  Client entrypoint for suggesting Wordle solutions.
  """
  return score(discard(misplaced, search(wordle, exclude(excluded, corpus))))


if __name__ == '__main__':
  wordle = 'g.ea.'
  excluded = 'rt'
  misplaced = ['.r...', '....t']

  for word_score in suggest(wordle, excluded, misplaced):
    print(f'{word_score.score:.7f} {word_score.word}')
