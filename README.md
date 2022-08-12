### Setup

The only prerequisite is Python 3.

```shell
$ git clone git@github.com:cadizm/wordle.git
$ cd wordle
$ python3 -m venv ~/.venvs/wordle
$ source ~/.venvs/wordle/bin/activate
```

### Usage

To run as a script, replace `wordle`, `excluded`, `included`, and `misplaced`
with appropriate values. The variable names are intended to be self-explanatory,
but see [the tests](test_wordle.py) for details on expected format. Then
execute normally:

```shell
$ python wordle.py
0.5000000 gleam
0.5000000 glean
```

To use as a library, `import wordle` and use the `suggest` entrypoint:

```python
from wordle import suggest

wordle = 'g.ea.'
excluded = 'rt'
included = 'gea'
misplaced = ['.r...', '....t']

for word_score in suggest(wordle, excluded, included, misplaced):
  print(f'{word_score.score:.7f} {word_score.word}')
```

To use as webapp, navigate to [dev.cadizm.com/wordle](https://dev.cadizm.com/wordle/)!
The interface is modified slightly, with individual inputs for `wordle` and `misplaced`
letters (`included` is also inferred from `misplaced`). Although the input mechanics
are different, the interface into [wordle.py](wordle.py) `suggest`
is the same, with the necessary transformations performed in the controller layer.

### Testing

```shell
$ python -m unittest discover
```

### TODO

[Blog](https://blog.cadizm.com/) post coming soon~
