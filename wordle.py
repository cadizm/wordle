import sys
import re


"""
TODO
  1.  Need some way to represent one of the following:
        a. include g at any position except 1
        b. exclude g from position 1
  2. Based on previous guess, suggest next guess (e.g., after using "ea"
     vowels on first try, suggest words with "ous", etc
  3. Productionize as webapp on cadizm.com
  4. Comments and blog post with complexity analysis
"""


def read_corpus(infile):
  return set(map(lambda line: line.strip(), open(infile).readlines()))


def prune(include, exclude, corpus):
  s = filter(lambda word: len(set(word) & set(exclude)) == 0, corpus)
  return filter(lambda word: len(set(word) & set(include)) == len(include), s)


def search(wordle, corpus):
  matches = lambda candidate: re.fullmatch(wordle, candidate)
  return sorted(list(filter(matches, corpus)))


if __name__ == '__main__':
  wordle = 'a..e.'
  include = 'eai'
  exclude = 'grtbusd'

  infile = './5-letter-words.txt'
  if len(sys.argv) > 1:
    infile = sys.argv[1]

  print('\n'.join(search(wordle, prune(include, exclude, read_corpus(infile)))))
