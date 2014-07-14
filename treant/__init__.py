import copy
import itertools

# node constructors

def mknode(value, children=[], attrs={}):
    return {'value': value,
            'attrs': attrs,
            'children': children}

def n(node_in):
    """'Smart' tuple interpreter.  First argument is
    always interpreted as the node value, any additional
    arguments are interpreted by type; if it's a list,
    consider it a list of children, if a dict consider
    it a dict or args.  Last one wins if there's multiple."""

    node = (node_in,) if isinstance(node_in, basestring) else node_in

    mknode_args = [node[0], [], {}]
    lookup = { list: 1, dict: 2}

    for v in node[1:]:
        mknode_args[lookup[type(v)]] = v

    return mknode(*mknode_args)

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

def tree(t, node_constructor=node):
    n = node_constructor(t)
    n['children'] = [tree(c, node_constructor=node_constructor)
                     for c
                     in children(n)]
    return n


# tree traversals

def preorder(tree):
    yield tree
    for c in children(tree):
        for n in preorder(c):
            yield n

def paths_preorder(tree, parents=[]):
    """Preorder generator through a tree (flat iterator through nodes
    in preorder) that yields paths to nodes, i.e. path = [n0, n1, n2]"""
    yield parents + [tree]
    for c in children(tree):
        for ptpair in paths_preorder(c, parents + [tree]):
            yield ptpair

# exhaustive search

def get(t, ks):
    """Search down a tree by nested values
    e.g.
        t = tree(['foo', ['bar', 'baz']])
        get(t, ['foo', 'bar', 'baz')  #=> baz node
        get(t, ['foo', 'bar', 'quux') #=> None

    TODO: Make me not O(n) for every level of search.
    """
    k = ks[0]

    if not value(t) == k:
        return None
    else:
        rest_ks = ks[1:]
        if rest_ks:
            for c in children(t):
                result = get(c, ks[1:])
                if result:
                    return result
            return None
        else:
            return t

def find_all_paths(tree, pred):
    """Find all paths where the last node in the path
    satisfies the given predicate"""
    return [p for p in paths_preorder(tree) if pred(p[-1])]

def find_all(tree, pred):
    """Find all nodes that satisfies the given predicate"""
    return [p[-1] for p in find_all_paths(tree, pred)]

def find_path_ex(tree, pred):
    """Find exclusive path; returns None if there's not exactly
    one matching path in the tree"""
    matches = find_all_paths(tree, pred)
    if len(matches) != 1:
        return None
    else:
        return matches[0]

def find_ex(tree, pred):
    """Find exclusive; returns None if there's not exactly
    one matching node in the tree"""
    match_path = find_path_ex(tree, pred)
    return match_path[-1] if match_path else None

# search helpers

def val_matches(v):
    return lambda node: value(node) == v

# pretty printer

def _pprint(tree, depth=0):
    yield "  " * depth + "- " + str(value(tree)) + " " + str(attrs(tree))
    for c in children(tree):
        for s in _pprint(c, depth=depth+1):
            yield s

def pprint(tree):
    return "\n".join(l for l in _pprint(tree))
