import treant
from treant import mknode, node, value, children, get, assoc
from treant import tree
from treant import preorder, paths_preorder

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
    assert False
