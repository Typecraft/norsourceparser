from norsourceparser.core.models import PosTreeContainer


def test_pos_tree_resolve():
    tree = 'pos("S" ( "S" ( "N" ("N" ("Epic"))))) ("V" ("V" ("V" ("Running")))))'

    resolved = PosTreeContainer.resolve_pos_tree(tree)
    assert len(resolved) == 2
    assert len(resolved[0]) == 2
    assert resolved[0][0] == 'N'
    assert resolved[0][1] == 'Epic'
    assert resolved[1][0] == 'V'
    assert resolved[1][1] == 'Running'



