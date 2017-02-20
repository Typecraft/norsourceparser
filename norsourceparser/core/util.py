import os
import json
import re


lex_fp = open(os.path.join(os.path.dirname(__file__), '../resources/lex.json'), 'r')
inflections_fp = open(os.path.join(os.path.dirname(__file__), '../resources/inflections.json'), 'r')
gloss_inflected_fp = open(os.path.join(os.path.dirname(__file__), '../resources/gloss_inflected.json'), 'r')
gloss_non_inflected_fp = open(os.path.join(os.path.dirname(__file__), '../resources/gloss_non_inflected.json'), 'r')
gloss_non_inflected_meanings_fp = open(os.path.join(os.path.dirname(__file__), '../resources/gloss_non_inflected_meanings.json'), 'r')
pos_all_fp = open(os.path.join(os.path.dirname(__file__), '../resources/pos_all.json'), 'r')

lex = json.load(lex_fp)
inflections = json.load(inflections_fp)
gloss_inflected = json.load(gloss_inflected_fp)
gloss_non_inflected = json.load(gloss_non_inflected_fp)
gloss_non_inflected_meanings = json.load(gloss_non_inflected_meanings_fp)
pos_all = json.load(pos_all_fp)

lex_fp.close()
inflections_fp.close()
gloss_inflected_fp.close()
gloss_non_inflected_fp.close()
gloss_non_inflected_meanings_fp.close()
pos_all_fp.close()

POS_CONVERSIONS = {
    "copnom": "COP",
    "s-adv": "ADV",
    "perf": "AUX",
    "indef-art": "DET",
    "stndadj": "ADJ",
    "n": "N",
    "tv": "V",
    "period": "PUN"
}

GLOSS_CONVERSIONS = {
    "ind": "INDEF",
    "m-or-f": "MASC",
    "mascorfem": "MASC",
    "m": "MASC",
    "masc": "MASC",
    "f": "FEM",
    "fem": "FEM",
    "sing": "SG",
    "plur": "PL"
}


def get_gloss(rule, default=None):
    if rule is None:
        return default
    if rule in GLOSS_CONVERSIONS:
        return GLOSS_CONVERSIONS[rule]
    elif rule in gloss_inflected:
        return gloss_inflected[rule]
    elif rule in gloss_non_inflected:
        return gloss_non_inflected[rule]
    else:
        # Time for special-cases
        if rule.rsplit("-").pop() == '-pn':
            return ""
        elif rule.rsplit("-").pop() == '-n1':
            return ""

        # Okey, lets try to match it against an end rule in our non-inflectional lookup
        rule_splitted = rule.rsplit("_")
        if len(rule_splitted) < 2:
            return default

        return gloss_non_inflected.get('_' + rule_splitted[1], default)


def get_pos(rule, default=None):
    if rule is None:
        return default
    if rule in POS_CONVERSIONS:
        return POS_CONVERSIONS[rule]
    elif rule in pos_all:
        return pos_all[rule]
    else:
        # Time for special-cases

        if rule.rsplit('-').pop() in ['-pn', '-n1']:
            return "Np"
        elif rule.rsplit("-").pop() in ['-comma', '-parenthesis', '-quotation', '-bracket', '-curlybracket', '-angledbracket']:
            return "PUN"

        return pos_all.get('_' + rule.rsplit("-").pop(), default)


def parse_lexical_entry_rule(name):
    """
    Takes a lexical_entry_rule and parses it.

    :param name:
    :return:
    """
    stem = pos = gloss = None
    name = name.split("_")

    if len(name) > 0:
        stem = name[0]

    if len(name) > 1:
        pos = name[1]

    if len(name) > 2:
        gloss = name[2]

    return [stem, pos, gloss]


def get_inflectional_rules(stem, rule):
    """
    Takes an inflectional rule, and returns an array of length three (or None) with the following information
        [Stem-Suffix, Suffix, Glosses]

    :param stem:
    :param rule:
    :return:
    """
    inflectional_rules = inflections.get(rule, None)
    if inflectional_rules is None:
        return None

    suffix_rules = inflectional_rules.get('suffix')

    for key in suffix_rules:
        if key == "*":
            continue
        if re.search(key + '$', stem) is not None:
            # We have found our proper matching end-case
            return [key, suffix_rules[key], map(lambda x: GLOSS_CONVERSIONS.get(x),
                                                inflectional_rules.get('attributes').values())]

    return None

