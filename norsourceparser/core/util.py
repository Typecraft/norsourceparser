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
    "indef-art": "DET",
    "stndadj": "ADJ",
    "n": "N",
    "tv": "V"
}

GLOSS_CONVERSIONS = {
    "ind": "INDEF",
    "m-or-f": "MASC",
    "m": "MASC",
    "f": "FEM",
    "sing": "SG",
    "plur": "PL"
}


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

