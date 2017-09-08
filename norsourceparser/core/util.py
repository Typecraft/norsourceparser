# coding=utf-8
import os
import json
import re

from norsourceparser.core.config import config

def open_resources_file(name):
    fp = open(os.path.join(os.path.dirname(__file__), '../resources/%s.json' % name), 'r')
    return json.load(fp)

verb_lex = open_resources_file('verb_lex')
verb_corrlist = open_resources_file('verb_corrlist')
noun_inflections = open_resources_file('noun_inflections')
gloss = open_resources_file('gloss')
meanings = open_resources_file('meanings')
pos = open_resources_file('pos')
concatenation_superfluity = open_resources_file('concatenation_superfluity')
dominating_mappings = open_resources_file('dominating_mappings')

POS_CONVERSIONS = {
    "copnom": "COP",
    "s-adv": "ADV",
    "indef-art": "DET",
    "stndadj": "ADJ",
    "n": "N",
    "tv": "V",
    "period": "PUN"
}

GLOSS_CONVERSIONS = {
    "ind": "INDEF",
    "def": "DEF",
    "m-or-f": "MASC",
    "mascorfem": "MASC",
    "m": "MASC",
    "n": "NEUT",
    "masc": "MASC",
    "f": "FEM",
    "fem": "FEM",
    "sing": "SG",
    "plur": "PL",
    "": ""
}


def get_gloss(rule, default=None):
    if rule is None:
        return default
    if rule in GLOSS_CONVERSIONS:
        return GLOSS_CONVERSIONS[rule]
    elif rule in gloss:
        return gloss[rule]
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

        return gloss.get('_' + rule_splitted[-1], default)


def get_pos(rule, default=None):
    if rule is None:
        return default
    if rule in POS_CONVERSIONS:
        return POS_CONVERSIONS[rule]
    elif rule in pos:
        return pos[rule]
    else:
        # Time for special-cases

        if rule.rsplit('-')[-1] in ['pn', 'n1']:
            return "Np"
        elif rule.rsplit("-")[-1] in ['comma', 'parenthesis', 'quotation', 'bracket', 'curlybracket', 'angledbracket']:
            return "PUN"

        # Okey, lets try to match it against an end rule in our non-inflectional lookup
        rule_splitted = rule.rsplit("_")

        if len(rule_splitted) < 2:
            return default

        return pos.get('_' + rule_splitted[-1], default)


def get_valency(rule, default=None):
    """
    Gets valency information from a (verb) rule. We check for an entry in the verb_lex dictionary
    for first the rule itself, and then the rule with a possible _vlxm suffix removed.

    :param rule:
    :param default:
    :return:
    """
    lex_corr = None
    if rule is None:
        return default, lex_corr
    elif rule in verb_lex:
        lex_corr = verb_lex[rule]
        if not lex_corr in verb_corrlist:
            if config.DEBUG:
                print("UNABLE TO FIND VALENCY_MAPPING FOR %s in CORRLIST" % lex_corr)
            return default, lex_corr
        return verb_corrlist[lex_corr], lex_corr
    elif rule.replace('_vlxm', '') in verb_lex:
        lex_corr = verb_lex[rule.replace('_vlxm', '')]
        if not lex_corr in verb_corrlist:
            if config.DEBUG:
                print("UNABLE TO FIND VALENCY_MAPPING FOR %s in CORRLIST" % lex_corr)
            return default, lex_corr
        return verb_corrlist[lex_corr], lex_corr

    return default, lex_corr


def split_lexical_entry(name):
    """
    Takes a lexical_entry_rule and splits it.

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

    :param stem: The stem of the word to get a rule for.
    :param rule: The rule as represented in a NorSource file.
    :return: An array with [Stem-Suffix, Suffix, Glosses]. The stem-suffix is
             the suffix of the stem, i.e. if we have løper as stem, we would possibly
             find 'er' as the stem-suffix, and something like 'te' as suffix - i.e.
             the conjugated version.
    """
    inflectional_rules = noun_inflections.get(rule, None)
    if inflectional_rules is None:
        return None

    glosses = filter(
        lambda x: x is not None,
        map(
            lambda x: GLOSS_CONVERSIONS.get(x),
            inflectional_rules.get('attributes').values()
        )
    )

    suffix_rules = inflectional_rules.get('suffix')
    if suffix_rules is None:
        return [None, None, glosses]

    default = None
    for key in suffix_rules:
        if key == "*":
            default = [key, suffix_rules[key], glosses]
            continue
        if re.search(key + '$', stem) is not None:
            # We have found our proper matching end-case
            return [key, suffix_rules[key], glosses]

    return default


def get_dominating_pos_rule(name, default=None):
    return dominating_mappings['pos'].get(name, default)


def get_dominating_gloss_rule(name, default=None):
    if name in dominating_mappings['pos']:
        return dominating_mappings['pos'].get(name, default)


def get_dominating_gloss_rule(name, default=None):
    if name in dominating_mappings['gloss']:
        return dominating_mappings['gloss'].get(name, default)


def prune_common_concatenation_superfluity(value):
    return concatenation_superfluity.get(value, value)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
