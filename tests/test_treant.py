import treant
from treant import mknode, node, value, children, get, assoc
from treant import tree
from treant import preorder, paths_preorder
from treant import find_all_paths, find_all, find_path_ex, find_ex
from treant import _pprint, pprint

from nose.tools import eq_

def test_mknode():
    bar = mknode('bar')
    baz = mknode('baz')
    assert mknode(
            'foo',
            [mknode('bar'), mknode('baz')],
            {'quux': 'wee'}) == {
                'value': 'foo',
                'children': [bar, baz],
                'attrs': {'quux': 'wee'}}

def test_node_string():
    assert treant.node('foo') == treant.mknode('foo', [], {})

def test_node_tuple_one():
    assert treant.node(('foo',)) == treant.mknode('foo')

def test_node_tuple_two():
    bar = mknode('bar')
    baz = mknode('baz')
    assert treant.node(('foo', [bar, baz])) == treant.mknode('foo', [bar, baz])

def test_node_dict():
    assert treant.node(
        {'value': 'foo', 'attrs': {'quux': 'wee'}}) == treant.mknode(
            value='foo', attrs={'quux': 'wee'})

def test_node_list():
    assert treant.node(['foo', 'bar', 'baz']) == treant.mknode('foo', ['bar', 'baz'])

def test_n_one_tuple():
    assert treant.n(('foo',)) == treant.mknode('foo')

def test_n_one_string_tup():
    assert treant.n(('foo')) == treant.mknode('foo')

def test_n_one_string():
    assert treant.n('foo') == treant.mknode('foo')

def test_n_many_list():
    bar = mknode('bar')
    baz = mknode('baz')
    assert treant.n(('foo', [bar, baz])) == treant.mknode('foo', [bar, baz])

def test_n_many_dict():
    attrs = { 'bar': 40, 'baz': 60 }
    assert treant.n(('foo', attrs)) == treant.mknode('foo', [], attrs)

def test_n_many_list_dict_in_order():
    bar = mknode('bar')
    baz = mknode('baz')
    children = [bar, baz]
    attrs = { 'quux': 40, 'weee': 60 }
    assert treant.n(('foo', children, attrs)) == treant.mknode('foo', children, attrs)

def test_n_many_list_dict_out_of_order():
    bar = mknode('bar')
    baz = mknode('baz')
    children = [bar, baz]
    attrs = { 'quux': 40, 'weee': 60 }
    assert treant.n(('foo', attrs, children)) == treant.mknode('foo', children, attrs)

def test_assoc_new_node_takes_newvalue():
    n0 = treant.mknode('foo', ['bar', 'baz'])

    new_children = ['quux', 'wee']
    n1 = treant.assoc(n0, 'children', new_children)
    assert children(n1) == new_children

def test_assoc_new_node_keeps_others():
    n0 = mknode('foo', ['bar', 'baz'])
    n1 = assoc(n0, 'children', ['quux', 'wee'])
    assert value(n1) == value(n0)

def test_assoc_old_node_non_destructive():
    old_children = ['bar', 'baz']
    new_children = ['quux', 'wee']

    n0 = mknode('foo', old_children)
    n1 = assoc(n0, 'children', new_children)

    assert children(n0) == old_children

def test_tree():
    nodes = ['foo', 'bar', 'baz']
    assert tree(nodes) == mknode('foo', [mknode('bar'), mknode('baz')])

def test_preorder():
    nodes = ['/', ['opt', 'framed', 'mcv']]
    traversal = [value(n) for n in preorder(tree(nodes))]
    assert traversal == ['/', 'opt', 'framed', 'mcv']

def test_get_present():
    nodes = ['/', ['opt', 'framed', 'mcv']]
    t = tree(nodes)
    n = get(t, ['/', 'opt', 'framed'])
    assert value(n) == 'framed'

def test_get_absent():
    nodes = ['/', ['opt', 'framed', 'mcv']]
    t = tree(nodes)
    assert get(t, ['/', 'opt', 'hello']) is None

def test_paths_preorder():
    nodes = ['/', ['opt', 'framed', 'mcv']]

    t = tree(nodes)
    root = get(t, ['/'])
    opt = get(t, ['/', 'opt'])
    framed = get(t, ['/', 'opt', 'framed'])
    mcv = get(t, ['/', 'opt', 'mcv'])

    paths = [p for p in paths_preorder(t)]

    eq_(paths,
        [[root],
         [root, opt],
         [root, opt, framed],
         [root, opt, mcv]])

def test__pprint():
    nodes = ['/', ['opt', 'framed', 'mcv']]
    t = tree(nodes)
    lines = [l for l in _pprint(t)]

    eq_(lines,
        ["- / {}",
         "  - opt {}",
         "    - framed {}",
         "    - mcv {}"])

def test_find_all_paths_hit_leaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ps = [p for p in find_all_paths(t, lambda n: value(n) == 'bin')]

    eq_(ps,
        [[root, opt, framed, framed_bin],
         [root, opt, mcv, mcv_bin]])

def test_find_all_paths_hit_nonleaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ps = [p for p in find_all_paths(t, lambda n: value(n) == 'framed')]

    eq_(ps, [[root, opt, framed]])

def test_find_all_paths_miss():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ps = [p for p in find_all_paths(t, lambda n: value(n) == 'nonsense!')]

    eq_(ps, [])

def test_find_all_hit_leaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ns = [n for n in find_all(t, lambda n: value(n) == 'bin')]

    eq_(ns, [framed_bin, mcv_bin])

def test_find_all_hit_nonleaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ns = [n for n in find_all(t, lambda n: value(n) == 'framed')]

    eq_(ns, [framed])


def test_find_all_miss():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin = preorder(t)
    ns = [n for n in find_all(t, lambda n: value(n) == 'nonsense!')]

    eq_(ns, [])

def test_find_path_ex_hit_leaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    p = find_path_ex(t, lambda n: value(n) == 'tests')

    eq_(p, [root, opt, mcv, mcv_tests])

def test_find_path_ex_hit_nonleaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    p = find_path_ex(t, lambda n: value(n) == 'mcv')

    eq_(p, [root, opt, mcv])

def test_find_path_ex_miss_absent():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    n = find_path_ex(t, lambda n: value(n) == 'nonsense!')

    eq_(n, None)

def test_find_path_ex_miss_nonunique():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    n = find_path_ex(t, lambda n: value(n) == 'bin')

    eq_(n, None)


def test_find_ex_hit_leaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    n = find_ex(t, lambda n: value(n) == 'tests')

    eq_(n, mcv_tests)

def test_find_ex_hit_nonleaf():
    nodes = ('/', [
                ('opt', [
                    ('framed', [
                        ('bin')]),
                    ('mcv', [
                        ('bin'),
                        ('tests')])])])
    t = tree(nodes)
    root, opt, framed, framed_bin, mcv, mcv_bin, mcv_tests = preorder(t)
    n = find_ex(t, lambda n: value(n) == 'mcv')

    eq_(n, mcv)
