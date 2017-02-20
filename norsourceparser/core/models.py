import re
import difflib

from . import config

from typecraft_python.models import Text, Phrase, Word, Morpheme

from norsourceparser.core.util import parse_lexical_entry_rule, get_pos, get_gloss, get_inflectional_rules


class AbstractSyntaxTree(object):
    """
    This abstract class is simply used to signify which methods a SyntaxTree _should_ have.
    """

    def __init__(self):
        pass

    def add_node(self, node):
        pass

    def remove_node(self, node):
        pass

    def __len__(self):
        return 0

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass


REDUCED_RULE_VALENCY_TOKEN = 0
REDUCED_RULE_POS = 1
REDUCED_RULE_MORPHOLOGICAL_BREAKUP = 2
REDUCED_RULE_GLOSSES = 3


class ReducedNode(object):
    """
    The ReducedNode class is a class representing a Word-token with a list of associated rules.

    The rules
    """
    def __init__(
        self,
        base_token=""
    ):
        self.base_token = base_token
        self.rules = {}

    def add_rule(self, rule_id, rule):
        """
        Adds a rule to this node
        :param rule_id:
        :param rule:
        :return:
        """
        self.rules[rule_id] = rule

    def remove_rule(self, rule_id):
        """
        Removes a rule from this node
        :param rule_id:
        :return:
        """
        del self.rules[rule_id]

    def has_rule(self, rule_id):
        """
        Returns true if this node has present a rule in its rule-dict.

        :param rule_id:  The rule id to lookup
        :return:  True or False
        """
        return rule_id in self.rules

    def get_completed_word_token(self):
        """
        Returns the completed word-token. This is not necessarily equal to the base_token, as we might have an
        overriding inflection. This will be then be reflected in the MORPHOLOGICAL_BREAKUP rule; if present.
        :return:
        """
        if REDUCED_RULE_MORPHOLOGICAL_BREAKUP in self.rules:
            return "".join(self.rules[REDUCED_RULE_MORPHOLOGICAL_BREAKUP])
        else:
            return self.base_token


class ReducedSyntaxTree(AbstractSyntaxTree):
    """
    The ReducedSyntaxTree represents a SyntaxTree in a state where each of it its three-branches has been reduced into
    a single node; A ReducedNode.

    We go through this state to easily be able to convert a Norsource SyntaxTree to TC-XML.
    """
    def __init__(self):
        super(ReducedSyntaxTree, self).__init__()
        self._nodes = []

    def add_node(self, node):
        """
        Adds a node to the syntax tree. O(1)
        :param node: A ReducedNode instance
        :return: void
        """
        assert isinstance(node, ReducedNode)
        self._nodes.append(node)

    def remove_node(self, node):
        """
        Removes a node from the syntax tree. O(n)
        :param index: An index
        :return:
        """
        assert isinstance(node, ReducedNode)
        self._nodes = list(filter(lambda x: x != node, self._nodes))

    def convert_to_tc(self):
        """
        Converts the Reduced SyntaxTree to a typecraft_python.models.Text object
        :return:
        """
        text = Text()
        phrase = Phrase()

        for node in self._nodes:
            word = Word()
            word.word = node.get_completed_word_token()
            word.pos = node.rules.get(REDUCED_RULE_POS, "")

            morphemes = []
            for morpheme_rule in node.rules.get(REDUCED_RULE_MORPHOLOGICAL_BREAKUP, []):
                morpheme = Morpheme()
                morpheme.morpheme = morpheme_rule

                morphemes.append(morpheme)
                word.add_morpheme(morpheme)

            gloss_rules = node.rules.get(REDUCED_RULE_GLOSSES, [])
            for i in range(len(gloss_rules)):
                gloss_rule = gloss_rules[i]
                if len(morphemes) <= i:
                    break
                morphemes[i].add_gloss(gloss_rule)

            phrase.add_word(word)

        phrase.phrase = " ".join(map(lambda word: word.word, phrase.words))
        text.add_phrase(phrase)

        return text

    def __iter__(self):
        """
        Returns an iterator over the nodes of this syntax tree. The nodes
        are iterated in order of addition.
        :return:
        """
        return self._nodes.__iter__()

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


class SyntaxTree(AbstractSyntaxTree):
    """
    Class representing a Syntax Tree as described by a NorSource XML-document.
    """

    def __init__(self, top=""):
        """
        Initializes the SyntaxTree
        :param (String) top: The top-node of the syntax-tree
        """
        super(SyntaxTree, self).__init__()
        self.top = top
        self._nodes = []

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
        self._nodes = list(filter(lambda x: x != node, self._nodes))

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

    def get_terminal_nodes(self):
        """
        Returns the terminal nodes of this SyntaxTree.
        :return:
        """
        return list(filter(lambda x: x.is_terminal, self))

    def reduce(self):
        """
        This method transforms the SyntaxTree into a ReducedSyntaxTree.

        This method is the primary source of difficulty in the conversion process, as it is here we try to
        deduce all word/morpheme rules for every word.

        The method in itself is fairly simple. It simply starts at each terminal node, traversing the tree upwards
        until it reaches the root. At each point it calls get_rule_from_partial_branch.


        :return:
        """
        reduced_tree = ReducedSyntaxTree()
        for node in self.get_terminal_nodes():
            base_token = node.name
            reduced_node = ReducedNode(base_token=base_token)

            partial_branch = [node]
            partial_node = node.parent
            # Traverse up the branch
            while partial_node is not None:
                partial_branch.append(partial_node)
                rules = self.get_rules_from_partial_branch(partial_branch)
                for rule in rules:
                    reduced_node.add_rule(rule[0], rule[1])

                partial_node = partial_node.parent
            reduced_tree.add_node(reduced_node)

        return reduced_tree

    @staticmethod
    def get_rules_from_partial_branch(partial_branch):
        """
        :param partial_branch:
        :return: A tuple with the rule type and the rule content
        """

        if len(partial_branch) < 2:
            return

        rules = []
        last_node = partial_branch[1]
        terminal = partial_branch[0]

        [stem, pos, gloss] = parse_lexical_entry_rule(last_node.name)
        converted_pos = get_pos(pos, None) or get_pos(last_node.name, None)
        converted_gloss = get_gloss(gloss, None) or get_gloss(last_node.name, None)

        if len(partial_branch) == 2:
            if converted_pos is None:
                print("UNABLE TO FIND POS FOR RULE: %s" % last_node.name)
            else:
                print("FOUND POS FOR: %s => %s" % (last_node.name, converted_pos))

            if converted_gloss is None:
                print("UNABLE TO FIND GLOSS FOR RULE: %s" % last_node.name)
            else:
                print("FOUND GLOSS FOR: %s => %s" % (last_node.name, converted_gloss))

        if len(partial_branch) == 2:
            # Here we are looking for a lexical entry
            if converted_pos is not None:
                rules.append([REDUCED_RULE_POS, converted_pos])

            # This happens on e.g. punctuations
            if stem is not None and pos is None and gloss is None:
                rules.append([REDUCED_RULE_POS, converted_pos])

            # We capture morphological breakup and glosses here.
            # This information may get overwritten later up the tree/branch. Yet
            # we still do this step in case we have some missing information later up the tree.
            if converted_pos in ['N', 'V', 'ADJ']:
                if stem != terminal.name:
                    rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [stem, re.sub("^"+stem, "", terminal.name)]])
                    # We do this here so we can capture the correct position
                    if converted_gloss is not None:
                        rules.append([REDUCED_RULE_GLOSSES, ["", converted_gloss]])
                else:
                    # Okey, we don't have any inflections here.
                    rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [stem]])
                    # We do this here so we can capture the correct position
                    if converted_gloss is not None:
                        rules.append([REDUCED_RULE_GLOSSES, [converted_gloss]])
            else:
                if converted_gloss is not None:
                    rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [terminal.name]])
                    rules.append([REDUCED_RULE_GLOSSES, [converted_gloss]])

        # We look for the special case of a bli_pass case here
        # And in this case, we don't want later rules to overwrite stuff.
        if partial_branch[1].name == 'bli_pass':
            rules.extend(SyntaxTree.get_bli_passive_rules(partial_branch))
        else:
            if converted_pos is "N":
                rules.extend(SyntaxTree.get_lexical_entry_rule(partial_branch))

            rules.extend(SyntaxTree.get_gloss_rules_from_partial_branch(partial_branch))
        return rules

    @staticmethod
    def get_lexical_entry_rule(partial_branch):
        rules = []
        if not len(partial_branch) < 3:
            return rules

        # Here we are looking for the inflectional rules for nouns
        last_node = partial_branch[-1]
        lexical_node = partial_branch[1]

        [stem, pos, _] = parse_lexical_entry_rule(lexical_node.name)
        pos = get_pos(pos, "")
        if pos != 'N':
            return rules

        inf_rules = get_inflectional_rules(stem, last_node.name)
        if inf_rules is None:
            return rules

        [current_suffix, suffix, glosses] = inf_rules

        morphological_breakup = [stem, re.sub("^"+current_suffix, "", suffix)]
        glosses = ["", glosses]

        rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, morphological_breakup])
        rules.append([REDUCED_RULE_GLOSSES, glosses])

        return rules

    @staticmethod
    def get_gloss_rules_from_partial_branch(partial_tree):
        """
        Tries to get rules for something other than a verb, noun or adjective. We do this simply by doing a lookup
        in the non-inflectional table. This is of course all encapsulated in the get_gloss method, so we just call that,
        fishing for luck.

        :param partial_tree:
        :return:
        """
        last_rule = partial_tree[-1].name

        maybe_gloss = get_gloss(last_rule)

        if maybe_gloss is not None:
            return [[REDUCED_RULE_GLOSSES, maybe_gloss.split(".")]]

        return []

    @staticmethod
    def get_bli_passive_rules(partial_branch):
        """
        This method checks for the special case of bli_passives.

        :param partial_branch:
        :return:
        """
        rules = []

        if len(partial_branch) == 3:
            lexical = partial_branch[1]
            if lexical.name == 'bli_pass':
                terminal = partial_branch[0]
                inflectional = partial_branch[2]

                rules.append([REDUCED_RULE_POS, 'V'])
                gloss_rules = []
                if inflectional.name == 'pres-infl_rule':
                    gloss_rules = ['PRES', 'PASS']
                elif inflectional.name == 'pret-finalstr_infl_rule':
                    gloss_rules = ['PRET', 'PASS']

                if 'bli' in terminal.name:
                    rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['bli', re.sub('^bli', '', terminal.name)]])
                else:
                    rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [terminal.name]])
                rules.append([REDUCED_RULE_GLOSSES, [gloss_rules]])
        return rules

    def __iter__(self):
        """
        Returns an iterator over the nodes of this syntax tree. The nodes
        are iterated in order of addition.
        :return:
        """
        return self._nodes.__iter__()

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


# This pattern should capture what we are looking for in the pos_tree expressions
pos_tree_pattern = '\("([\w-]+)" \("(\w+)"\)\)'


class PosTreeContainer(object):
    """
    Class that contains pairs of
        <input> <posTree> tag contents.

    We use this class to parse the simpler input->posTree pairs
    """

    def __init__(self):
        self._pairs = []

    def add_pair(self, input, pos_tree):
        self._pairs.append((input, pos_tree))

    def resolve(self):
        """
        Resolves the PosTreeContainer.

        This method simply goes through each pair, and resolves the pos_tree information into word <-> POS tuples.
        :return:
        """
        pairs = self._pairs
        self._pairs = []
        for pair in pairs:
            (input, pos_tree) = pair

            pos_tree = PosTreeContainer.resolve_pos_tree(pos_tree)
            self.add_pair(input, pos_tree)

    @staticmethod
    def resolve_pos_tree(pos_tree):
        """
        Resolves a pos_tree. The a posTree tag by default contains data something alike

            ("S" ( "S" ( "N" ("N" ("Epic"))))) ("V" ("V" ("V" ("Running")))))

        The main thing to extract here is the innermost (POS ("Word")) for each case.

        A typical result of the above posTree tag would be

            [ ('N', 'Epic'), ('V', 'Running') ]
        :param pos_tree:
        :return:
        """
        # The pattern should capture what we are looking for
        return re.findall(pos_tree_pattern, pos_tree, re.UNICODE)

    def convert_to_tc(self):
        """
        Converts the PosTreeContainer into a typecraft_python.model.Text.

        This is a very straightforward process
        :return:
        """
        text = Text()
        text.title = "Converted Norsource"

        for pair in self._pairs:
            (input, pos_tree) = pair
            phrase = Phrase()
            phrase.phrase = input

            for word_pos_entry in pos_tree:
                word = Word()
                word.word = word_pos_entry[1]
                word.pos = word_pos_entry[0]
                phrase.add_word(word)

            text.add_phrase(phrase)

        return text
