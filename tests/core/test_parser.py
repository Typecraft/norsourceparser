from norsourceparser.core.models import SyntaxTree
from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.models import Text
from typecraft_python.parsing.parser import Parser as TParser
import xml.etree.ElementTree as ET
import os

file_name = os.path.join(os.path.dirname(__file__), '../resources/norsource_1.xml')
pos_file_name = os.path.join(os.path.dirname(__file__), '../resources/norsource_pos.xml')


def test_load_file():
    parser = Parser()
    tree = parser.load_file(file_name)

    assert isinstance(tree, SyntaxTree)
    assert len(tree) == 31   # See file for more information
    assert len(tree.get_terminal_nodes()) == 8


def test_parse_file():
    parser = Parser()
    tc_file = parser.parse_file(file_name)

    assert isinstance(tc_file, Text)


def test_parse_pos_tree_file():
    result = PosTreeParser.parse_file(pos_file_name)
    print(unicode(result))
    print(ET.tostring(TParser.convert_texts_to_etree([result])))

    assert isinstance(result, Text)
