from norsourceparser.core.models import UnresolvedSyntaxTree, SyntaxTree, SyntaxNode


def test_unresolved_add_node():
    """
    Test the add_node function of UnresolvedSyntaxTree
    :return:
    """
    node_1 = SyntaxNode(name="kebab_n_neut")
    u_tree = UnresolvedSyntaxTree()
    u_tree.add_node(node_1)
    assert len(u_tree) == 1
    assert node_1 in u_tree


def test_unresolved_remove_node():
    """
    Test the remove_node function of UnresolvedSyntaxTree
    :return:
    """
    node_1 = SyntaxNode(name="kebab_n_neut")
    u_tree = UnresolvedSyntaxTree()
    u_tree.add_node(node_1)
    u_tree.remove_node(node_1)
    assert len(u_tree) == 0
    assert node_1 not in u_tree


def test_resolve_simple():
    """
    Test a simple resolve, where we have no relationships
    :return:
    """
    node_1 = SyntaxNode(name="kebab_n_neut")
    node_2 = SyntaxNode(name="er_tv")
    node_3 = SyntaxNode(name="digg_adj")

    u_tree = UnresolvedSyntaxTree()
    u_tree.add_node(node_1)
    u_tree.add_node(node_2)
    u_tree.add_node(node_3)

    resolved_tree = u_tree.resolve()

    assert isinstance(resolved_tree, SyntaxTree)
    assert len(resolved_tree) == 3
    assert node_1 in resolved_tree
    assert node_2 in resolved_tree
    assert node_3 in resolved_tree


def test_resolve_parenthood_correct():
    node_1 = SyntaxNode(id="n1", name="kebab_n_neut")
    node_2 = SyntaxNode(id="n2", name="er_tv", parent_id="n1")
    node_3 = SyntaxNode(id="n3", name="digg_adj", parent_id="n2")

    u_tree = UnresolvedSyntaxTree()
    u_tree.add_node(node_1)
    u_tree.add_node(node_2)
    u_tree.add_node(node_3)

    u_tree.resolve()

    assert node_1.parent == None
    assert node_2.parent == node_1
    assert node_3.parent == node_2


def test_resolve_complex_structure():
    pass
