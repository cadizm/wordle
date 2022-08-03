import sys
import re
from collections import namedtuple


class Wordle:
  """
  """


def read_corpus(infile):
  return set(map(lambda x: x.strip(), open(infile).readlines()))


def prune(letters, corpus):
  f = lambda x: len(set(x).intersection(set(letters))) == 0
  return filter(f, corpus)


def search(candidate, corpus):
  f = lambda x: re.fullmatch(candidate, x) is not None
  return sorted(list(filter(f, corpus)))


if __name__ == '__main__':
  candidate = '.o.ly'
  exclude = 'qwertuasdgbm'

  print(search(candidate, prune(exclude, read_corpus(sys.argv[1]))))
