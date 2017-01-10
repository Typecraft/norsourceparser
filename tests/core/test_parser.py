from norsourceparser.core.models import SyntaxTree
from norsourceparser.core.parser import Parser
import os

file_name = os.path.join(os.path.dirname(__file__), '../resources/norsource_1.xml')


def test_load_file():
    parser = Parser()
    tree = parser.load_file(file_name)

    assert isinstance(tree, SyntaxTree)
    assert len(tree) == 31   # See file for more information
    assert len(tree.get_terminal_nodes()) == 8

    print(tree)

