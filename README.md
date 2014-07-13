treant
======

Simple tree operations in Python

Trees data strutures are pervasive in computer science, even for the
most practical tasks such as organizing files on a file system.
Treant provides basic tree construction and operations in as simple a
way as possible.

Quickstart
----------

```python
import treant

t = treant.tree(
    ('/', [
        ('home', [
            ('jane', []),
            ('john', [])]),
        ('opt', [
            ('robots', [
                ('bin', [])])])]))

```

Given such a data struture parsed into a tree, you can do stuff like:

- Iterate through all the nodes / values in a tree in a specific order
  (preorder, inorder, postorder) (forthcoming)
- Find whether a specific node / value is in the tree
- List all paths
