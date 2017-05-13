from norsourceparser.core.models import SyntaxTree
from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.models import Text
from typecraft_python.parsing.parser import Parser as TParser
import xml.etree.ElementTree as ET
import os

file_name = os.path.join(os.path.dirname(__file__), '../resources/norsource_2.xml')
pos_file_name = os.path.join(os.path.dirname(__file__), '../resources/norsource_pos.xml')


def test_load_file():
    parser = Parser()
    tree = parser.load_file(file_name)

    assert isinstance(tree, ET.ElementTree)


def test_parse_file():
    parser = Parser()
    tc_file = parser.parse_file(file_name)

    assert isinstance(tc_file, Text)

    print(tc_file.phrases[0].global_tags[0].name)
    print(tc_file.__str__())


def test_parse_pos_tree_file():
    result = PosTreeParser.parse_file(pos_file_name)

    assert isinstance(result, Text)
