from norsourceparser.core.models import SyntaxNode


def test_instantiate():
    node = SyntaxNode()

    assert node.beg == ""
    assert node.end == ""
    assert node.id == ""
    assert node.name == ""
    assert node.num == ""
    assert node.parent_id == ""
    assert node.parent is None
    assert node.pct == ""
    assert node.is_terminal == False
