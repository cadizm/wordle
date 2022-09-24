import os
import sys
import re
from functools import reduce
from itertools import chain
from collections import defaultdict, namedtuple


def read_lexicon(infile):
  """
  Read infile (dictionary with 1 word per line) and return its contents as a set.
  """
  return set(map(lambda line: line.strip(), open(infile).readlines()))


def include(letters, lexicon):
  """
  Return words in lexicon that include all letters in `letters`.
  """
  return set(filter(lambda word: set(word) & set(letters) == set(letters), lexicon))


def exclude(letters, lexicon):
  """
  Return words in lexicon that exclude all letters in `letters`.
  """
  return set(filter(lambda word: set(word) & set(letters) == set(), lexicon))


def same_letter_occurrence(wordle):
  """
  Return lambda accepting a single argument `word` answering the following predicate: for all
  letters shared between `word` and `wordle`, if the number of occurences of `letter` equals
  the number of occurrences of `letter` in `wordle`, return True; False otherwise.
  """
  return lambda word: all([occurrence(letter, word) == occurrence(letter, wordle) \
      for letter in set(word) & set(wordle)])


def occurrence(letter, s):
  """
  Return the number of occurrences of `letter` in string `s`.
  """
  return sum([1 if v == letter else 0 for v in s])


def matches(regex):
  """
  Return lambda returning True when its argument matches `regex`.
  """
  return lambda x: re.fullmatch(f'^{regex}$', x)


def search(wordle, lexicon):
  """
  Search words in lexicon matching the regular expression specified in `wordle`.
  """
  return set(filter(matches(wordle), lexicon))


def union(sets):
  """
  Return the union of the list of sets in `sets`.
  """
  return reduce(lambda x, y: x.union(y), sets, set())


def discard(misplaced, lexicon):
  """
  Discard from lexicon words matching regular expressions in list `misplaced`.
  """
  return set(lexicon) - union(map(lambda wordle: search(wordle, lexicon), misplaced))


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


lexicon = read_lexicon(os.path.abspath(os.path.join(os.path.dirname(__file__), '5-letter-words.txt')))

def suggest(wordle, excluded, misplaced):
  """
  Client entrypoint for suggesting Wordle solutions.
  """
  # infer what must be included using wordle and misplaced
  included = ''.join(set(chain(wordle, *misplaced)) - set('.'))
  # remove letters in wordle from excluded
  exclusions = exclude(set(excluded) - set(wordle), lexicon)
  # only keep words with same letter occurrence as wordle letters when wordle overlaps excluded
  exclusion_overlap = (set(wordle) - set('.')) & set(excluded)
  if exclusion_overlap:
    exclusions = filter(same_letter_occurrence(wordle), exclusions)

  return score(discard(misplaced, search(wordle, include(included, exclusions))))


if __name__ == '__main__':
  wordle = 'cla.s'
  excluded = 'gretbin'
  misplaced = ['...a.', '.a...', '...l.']

  for word_score in suggest(wordle, excluded, misplaced):
    print(f'{word_score.score:.7f} {word_score.word}')
