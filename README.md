treant
======

Simple tree operations in Python

![buildstatus](https://circleci.com/gh/framed-data/treant.png?circle-token=5547972ae8a78299424cfe0a98fd94167a7f2054)

Trees data strutures are pervasive in computer science, even for the
most practical tasks such as organizing files on a file system.
Treant provides basic tree construction and operations in as simple a
way as possible.

Quickstart
----------

```python
import treant
from treant import value

t = treant.tree(
    ('/', [
        ('home', [
            ('jane', []),
            ('john', [
                ('bin')])]),
        ('opt', [
            ('robots', [
                ('bin', [])])])]))

path = treant.find_path_ex(t, lambda n: value(n) == 'robots')
# => [root_node>, <opt_node>, <robots_node>]

path_values = [value(n) for n in path]
# => ['/', 'opt', 'robots']

node = treant.find_ex(t, lambda n: value(n) == 'jane')
# => <jane_node>

node = treant.find_ex(t, lambda n: value(n) == 'nonsense!')
# => None

node = treant.find_ex(t, lambda n: value(n) == 'bin')
# => None   # find_ex only returns a value if the match is unique

node = treant.find_all(t, lambda n: value(n) == 'bin')
# => [<john_bin_node>, <robots_bin_node>]  # find_all returns all matches

```
