"""
This file contains methods for translation norsource rules into rules we can
convert easily to a Typeraft compatible format.
"""
import re

from norsourceparser.core.config import config
from norsourceparser.core.constants import REDUCED_RULE_POS, REDUCED_RULE_GLOSSES, REDUCED_RULE_MORPHOLOGICAL_BREAKUP, \
    REDUCED_RULE_VALENCY
from norsourceparser.core.util import get_pos, get_inflectional_rules, get_valency
from norsourceparser.core.util import split_lexical_entry, get_gloss


def get_rules_from_partial_branch(partial_branch):
    """
    This method is the main `entry-point` for inferring rules from a branch.

    The method will analyse the branch for POS and GLOSS-tags, and possibly morphological
    breakups.

    :param partial_branch: A list of branch-entries.
    :return: Array of rules
    """

    # If we are at the terminal, we do nothing just yet.
    if len(partial_branch) < 2:
        return

    rules = []
    second_node = partial_branch[1]
    terminal = partial_branch[0]

    # With the terminal and second node, we can get information
    # from the lexical entry
    [stem, pos, gloss] = split_lexical_entry(second_node.name)
    pos = get_pos(pos, None) or get_pos(second_node.name, None)
    gloss = get_gloss(gloss, None) or get_gloss(second_node.name, None)

    # If
    if len(partial_branch) == 2 and config.DEBUG:
        if pos is None:
            print("UNABLE TO FIND POS FOR RULE: %s" % second_node.name)

    if len(partial_branch) == 2:
        # If we only have access to the lexical entry, we return what rules
        # we can from here.

        # Verbs might yield some valency information here
        if pos == "V":
            rules.extend(get_verb_valency_rule(partial_branch))

        rules.extend(parse_lexical_entry(terminal, stem, pos, gloss))
        return rules

    if 'bli_pass' in partial_branch[1].name:
        # We look for the special case of a bli_pass case here
        rules.extend(get_bli_passive_rules(partial_branch))
    else:
        rules.extend(get_gloss_rules_from_partial_branch(partial_branch))

        if pos == "N":
            # If the pos is a Noun, we look for the special noun inflectional rules
            rules.extend(get_noun_inflectional_rule(partial_branch))

    return rules


def parse_lexical_entry(terminal, stem, pos, gloss):
    """
    This method helps us to parse a lexical entry.
    To do this, we need the extracted stem pos and gloss from the rule,
    as well as the terminal.

    :param terminal: The terminal node, which will contain the dictonary-form of the
                     word we are trying to associate rules with.
    :param stem: The parsed stem-form of the word.
    :param pos: The POS-tag of the word.
    :param gloss: Any gloss-tags so far found of the word.
    :return: An array of rules.
    """
    rules = []

    # Here we are parsing the lexical entry of the branch
    if pos is not None:
        rules.append([REDUCED_RULE_POS, pos])

    # This happens on e.g. punctuations
    if stem is not None and pos is None and gloss is None:
        rules.append([REDUCED_RULE_POS, pos])

    # We capture morphological breakup and glosses here.
    # This information may get overwritten later up the tree/branch. Yet
    # we still do this step in case we have some missing information later up the tree.
    if pos in ['N', 'V', 'ADJ']:
        if stem != terminal.name and stem in terminal.name:
            rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [stem, re.sub("^"+stem, "", terminal.name)]])
            # We do this here so we can capture the correct position
            if gloss is not None:
                rules.append([REDUCED_RULE_GLOSSES, ["", gloss]])
        else:
            if stem not in terminal.name:
                # We have morphology, but it is non-concatenative
                rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [terminal.name]])
            else:
                # We have no morpholog at all here, we don't have any inflections here.
                rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [stem]])
            # We do this here so we can capture the correct position
            if gloss is not None:
                rules.append([REDUCED_RULE_GLOSSES, [gloss]])
    else:
        rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [terminal.name]])
        if gloss is not None:
            rules.append([REDUCED_RULE_GLOSSES, [gloss]])

    return rules


def get_noun_inflectional_rule(partial_branch):
    """
    This method helps us to parse an inflectional rule for a noun.

    The method accepts a partial branch, but only proceeds if the branch is at least
    of length 3. We allow this flexibility as we might not want to control the method-calls to
    this method in the calling methods.

    If the POS of the branch is found not to be a noun, we simply return.

    :param partial_branch: A partial branch.
    :return: An array, potentially filled with rules.
    """
    rules = []
    if len(partial_branch) < 3:
        return rules

    # Here we are looking for the inflectional rules for nouns
    last_node = partial_branch[-1]
    lexical_node = partial_branch[1]

    [stem, pos, _] = split_lexical_entry(lexical_node.name)
    pos = get_pos(pos, None) or get_pos(lexical_node.name, None)
    if pos != 'N':
        return rules

    inf_rules = get_inflectional_rules(stem, last_node.name)
    if inf_rules is None:
        return rules

    [current_suffix, suffix, glosses] = inf_rules
    if glosses is None and config.DEBUG:
        print("NONE GLOSSES", glosses)

    if current_suffix is None or suffix is None:
        # This happens on the rule pl_ind_n_short_0_irule
        rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [stem]])
        rules.append([REDUCED_RULE_GLOSSES, [".".join(glosses)]])
    else:
        if current_suffix == '*':
            morphological_breakup = [stem, suffix]
        else:
            morphological_breakup = [stem, re.sub("^"+current_suffix, "", suffix)]

        glosses = ["", ".".join(glosses)]

        rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, morphological_breakup])
        rules.append([REDUCED_RULE_GLOSSES, glosses])

    return rules


def get_gloss_rules_from_partial_branch(partial_tree):
    """
    Tries to get rules for something other than a verb, noun or adjective. We do this simply by doing a lookup
    in the non-inflectional table. This is of course all encapsulated in the get_gloss method, so we just call that,
    fishing for luck.

    :param partial_tree:
    :return: An array of rules
    """
    last_rule = partial_tree[-1].name
    lexical_rule = partial_tree[1].name
    terminal = partial_tree[0].name
    [stem, pos, _] = split_lexical_entry(lexical_rule)
    pos = get_pos(pos, None) or get_pos(lexical_rule, None)

    maybe_gloss = get_gloss(last_rule)

    if maybe_gloss is not None:
        if pos in ['N', 'ADJ', 'V']:
            if stem != terminal and stem in terminal:
                # This means we have some inflectional rule, and should
                # add the gloss to the suffix
                return [[REDUCED_RULE_GLOSSES, ["", maybe_gloss]]]
        return [[REDUCED_RULE_GLOSSES, [maybe_gloss]]]

    return []


def get_bli_passive_rules(partial_branch):
    """
    This method checks for the special case of bli_passives.

    :param partial_branch:
    :return: An array of rules
    """
    rules = []

    if len(partial_branch) == 3:
        lexical = partial_branch[1]
        if 'bli_pass' in lexical.name:
            terminal = partial_branch[0]
            inflectional = partial_branch[2]

            rules.append([REDUCED_RULE_POS, 'V'])
            gloss_rules = []
            if inflectional.name == 'pres-infl_rule':
                gloss_rules = 'PRES.PASS'
            elif inflectional.name == 'pret-finalstr_infl_rule':
                gloss_rules = 'PRET.PASS'

            if 'bli' in terminal.name:
                rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['bli', re.sub('^bli', '', terminal.name)]])
            else:
                rules.append([REDUCED_RULE_MORPHOLOGICAL_BREAKUP, [terminal.name]])
            rules.append([REDUCED_RULE_GLOSSES, [gloss_rules]])
    return rules


def get_verb_valency_rule(partial_branch):
    """
    This method tries to get a valency rule for a verb.

    :param partial_branch:
    :return:
    """
    valency = get_valency(partial_branch[-1].name)
    if valency:
        return [[REDUCED_RULE_VALENCY, valency]]
    return []
