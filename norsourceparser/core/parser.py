import os
import xml.etree.ElementTree as ET

from norsourceparser.core.models import UnresolvedSyntaxTree, SyntaxNode, PosTreeContainer

NORSOURCE_ROOT_TAG = 'parse'
NORSOURCE_SYNTAXTREE_TAG = 'syntax-tree'
NORSOURCE_NODE_TAGS = ['terminal', 'node']


class PosTreeParser(object):

    @staticmethod
    def parse(norsource=""):
        """
        Parses a Norsource in string-form using the posTree pipeline.

        :param norsource:
        :return:
        """
        container = PosTreeParser.load_file(norsource)
        container.resolve()
        return container.convert_to_tc()

    @staticmethod
    def parse_file(norsource):
        """
        Parses a Noursource in file-form using the posTree pipeline.

        :param norsource:
        :return:
        """
        container = PosTreeParser.load_file(norsource)
        container.resolve()
        return container.convert_to_tc()

    @staticmethod
    def load(string_content):
        """
        Loads a Norsource in string-form into a PosTreeContainer.

        :param string_content:
        :return:
        """
        element_tree = ET.fromstring(string_content)
        return PosTreeParser.create_pos_tree_container_from_etree(element_tree)

    @staticmethod
    def load_file(filename):
        """
        Loads a Norsource resource in file-form into a PosTreeContainer.

        :param filename:
        :return:
        """
        element_tree = ET.parse(filename)
        return PosTreeParser.create_pos_tree_container_from_etree(element_tree)

    @staticmethod
    def create_pos_tree_container_from_etree(element_tree):
        """
        This is the first heavy-duting parsing method in the pos-tree pipeline. It takes an ElementTree, and
        converts it into a PosTreeContainer.

        :param element_tree:
        :return:
        """
        pos_tree_container = PosTreeContainer()
        root_el = element_tree.getroot()

        for parse_el in root_el.iter('parse'):
            input_el = parse_el.find('input')
            pos_tree_el = parse_el.find('posTree')
            if input_el is None or pos_tree_el is None:
                continue

            input = input_el.text
            pos_tree = pos_tree_el.text
            print(input)
            print(pos_tree)
            pos_tree_container.add_pair(input, pos_tree)

        return pos_tree_container


class Parser(object):
    def __init__(self):
        pass

    def parse(self, norsource=""):
        """
        This method parses a Norsource XML represented as a string, into a Typecraft text object.

        :param (String) norsource: A Norsource file as a string
        :return Text: A Typecraft Text
        """
        syntax_tree = self.load(norsource)
        reduced_tree = syntax_tree.reduce()
        return reduced_tree.convert_to_tc()

    def parse_file(self, norsource):
        """
        This method parses a Norsource XML represented as a file-path, into a Typecraft text object.

        :param (String) norsource: A file path to a norsource file
        :return Text: A Typecraft Text
        """
        syntax_tree = self.load_file(norsource)
        reduced_tree = syntax_tree.reduce()
        return reduced_tree.convert_to_tc()

    def load(self, string=""):
        """
        This method takes a string representing a Norsource XML file, and creates from it a SyntaxTree.
        :return:
        """
        element_tree = ET.fromstring(string)
        return self.create_syntax_tree_from_et(element_tree)

    def load_file(self, filename):
        """
        This method takes a filename representing a Norsource XML file, and creates from it a SyntaxTree.
        :param filename:
        :return:
        """
        if not os.path.exists(filename):
            raise Exception("Critical error: File %s does not exist" % filename)
        element_tree = ET.parse(filename)

        return self.create_syntax_tree_from_et(element_tree)

    def create_syntax_tree_from_et(self, element_tree):
        """
        This is the first of the heavy-duty parsing methods. It takes an xml.ElementTree, and parses this into a
        SyntaxTree.

        :param (ElementTree) element_tree: An ElementTree representation of a Norsource file.
        :return:
        """
        root = element_tree.getroot()
        if not root.tag == 'parse':
            raise Exception("Critical error parsing file: Root element must be of type <parse>")

        syntax_tree_et = root.find('syntax-tree')
        if syntax_tree_et is None:
            raise Exception("Critical error parsing file: Missing <syntax-tree> node. This node cannot be omitted")

        # Okey, the document is well-formed (enough), lets start parsing
        top = syntax_tree_et.attrib.get('top')
        u_syntax_tree = UnresolvedSyntaxTree(top=top)
        for node_et in syntax_tree_et:
            if node_et.tag not in NORSOURCE_NODE_TAGS:
                raise Exception("Critical error parsing file: Found unknown element of type %s" % node_et.name)
            u_syntax_tree.add_node(Parser._parse_et_node_to_syntax_node(node_et))

        return u_syntax_tree.resolve()

    @staticmethod
    def _parse_et_node_to_syntax_node(et_node):
        """
        Parses an ElementTree node representing a node into a SyntaxNode
        :param (ElementTree) et_node:
        :return (SyntaxNode):
        """
        attributes = et_node.attrib
        return SyntaxNode(
            id=attributes.get('id'),
            name=attributes.get('name'),
            beg=attributes.get('beg'),
            end=attributes.get('end'),
            parent_id=attributes.get('parent'),
            num=attributes.get('num'),
            pct=attributes.get('pct'),
            is_terminal=et_node.tag == 'terminal'
        )

