import copy
import itertools

# node constructors

def mknode(value, children={}, attrs={}):
    return {'value': value,
            'attrs': attrs,
            'children': children}

def node(node):
    types = {str: lambda s: mknode(s),
             tuple: lambda t: mknode(*t),
             list: lambda l: mknode(l[0], l[1:]),
             dict: lambda d: mknode(**d)}
    node_type = type(node)
    return types[node_type](node)

# node operations

def assoc(d, k, v):
    """Copy-associate a kv pair into a dictionary"""
    d2 = copy.copy(d)
    d2[k] = v
    return d2

# lightly abstract the accessors over the underlying data structure

def attrs(node):
    return node['attrs']

def value(node):
    return node['value']

def children(node):
    return node['children']

# tree constructor

def tree(t):
    n = node(t)
    n['children'] = [tree(c) for c in children(n)]
    return n

# simple tree operations

def get(t, ks):
    """Search down a tree by nested values
    e.g.
        t = tree(['foo', ['bar', 'baz']])
        get(t, ['foo', 'bar', 'baz')  #=> baz node
        get(t, ['foo', 'bar', 'quux') #=> None

    TODO: Make me not O(n) for every level of search.
    """
    if not ks:
        return t
    k = ks[0]
    for c in children(t):
        if value(c) == k:
            return get(c, ks[1:])
    return None

# tree traversals

def preorder(tree):
    yield tree
    for c in children(tree):
        for n in preorder(c):
            yield n

def paths_preorder(tree, parents=[]):
    """Preorder generator through a tree (flat iterator through nodes
    in preorder) that yields 2-tuples of (path_to_node, node)"""
    yield (parents + [tree], tree)
    for c in children(tree):
        for ptpair in paths_preorder(c, parents + [tree]):
            yield ptpair
