

class SyntaxNode(object):
    def __init__(
        self,
        beg="",
        end="",
        id="",
        name="",
        num="",
        parent_id="",
        parent=None,
        pct="",
        is_terminal=False
    ):
        """
        Initializes a syntax Node
        :param (String) beg: <String>
        :param (String) end:
        :param (String) id:
        :param (String) name:
        :param (String) num:
        :param (String) parent_id: The string-id of the parent
        :param (SyntxNode) parent:
        :param (String) pct:
        """
        # This is the only parameter we really care about strictly being correct
        assert parent is None or isinstance(parent, SyntaxNode)
        self.beg = beg
        self.end = end
        self.id = id
        self.name = name
        self.num = num
        self.parent_id = parent_id
        self.parent = parent
        self.pct = pct
        self.is_terminal = is_terminal


class SyntaxTree(object):
    """
    Class representing a Syntax Tree as described by a NorSource XML-document.
    """

    def __init__(self, top=""):
        """
        Initializes the SyntaxTree
        :param (String) top: The top-node of the syntax-tree
        """
        self.top = top
        self._nodes = []
        self._node_dict = {}  # Extra storage for quick retrieval

    def add_node(self, node):
        """
        Adds a node to the syntax tree. O(1)
        :param node: A SyntaxNode instance
        :return: void
        """
        assert isinstance(node, SyntaxNode)
        self._nodes.append(node)

    def remove_node(self, node):
        """
        Removes a node from the syntax tree. O(n)
        :param index: An index
        :return:
        """
        assert isinstance(node, SyntaxNode)
        self._nodes = filter(lambda x: x != node, self._nodes)

    def find_node_by_id(self, id):
        """
        Finds a node by id.

        :param id:
        :return:
        """
        if id is None:
            return None
        for node in self._nodes:
            if node.id == id:
                return node
        return None

    def __len__(self):
        """
        Returns the size of the syntax tree, i.e. the node count
        :return:
        """
        return len(self._nodes)

    def __contains__(self, item):
        """
        Checks if an item is contained in this syntax tree, i.e. in this nodes
        :param item:
        :return:
        """
        return item in self._nodes


class UnresolvedSyntaxTree(SyntaxTree):
    """
    Class used while constructing a Syntax Tree.

    The class represents a SyntaxTree which has not yet resolved proper parenthood / dependencies / links.

    We use this class temporarily while parsing a NorSource XML-document to throw all our information at before
    resolving any relationships.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the instance, creating an empty nodelist
        """
        super(UnresolvedSyntaxTree, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        Resolves the Unresvoled Tree, creating a new Syntax tree with everything wrapped up.

        A new SyntaxTree is constructed, but the Nodes are modified in-place.
        :return:
        """
        resolved = SyntaxTree()

        for node in self._nodes:
            parent = self.find_node_by_id(node.parent_id)
            node.parent = parent
            resolved.add_node(node)

        return resolved

