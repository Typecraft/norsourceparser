# coding=utf-8
from norsourceparser.core.constants import REDUCED_RULE_POS, REDUCED_RULE_MORPHOLOGICAL_BREAKUP, REDUCED_RULE_GLOSSES
from norsourceparser.core.models import SyntaxNode
from norsourceparser.core.rules import parse_lexical_entry


def test_parse_lexical_entry_with_typical_input():
    rules = parse_lexical_entry(SyntaxNode(name='løper'), 'løpe', 'V', None)

    assert len(rules) == 2
    assert [REDUCED_RULE_POS, 'V'] in rules
    assert [REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['løpe', 'r']] in rules


def test_parse_lexical_entry_with_terminal_equal_to_stem():
    rules = parse_lexical_entry(SyntaxNode(name='løpe'), 'løpe', 'V', None)

    assert len(rules) == 2
    assert [REDUCED_RULE_POS, 'V'] in rules
    assert [REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['løpe']] in rules


def test_parse_lexical_entry_with_gloss():
    rules = parse_lexical_entry(SyntaxNode(name='Hunden'), 'Hunden', 'N', 'SG.DEF.MASC')

    assert len(rules) == 3
    assert [REDUCED_RULE_POS, 'N'] in rules
    assert [REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['Hunden']] in rules
    assert [REDUCED_RULE_GLOSSES, ['SG.DEF.MASC']] in rules


def test_parse_lexical_entry_non_NVADJ_returns_breakup():
    rules = parse_lexical_entry(SyntaxNode(name='Fortere'), 'Fortere', 'ADV', None)

    assert len(rules) == 2
    assert [REDUCED_RULE_POS, 'ADV'] in rules
    assert [REDUCED_RULE_MORPHOLOGICAL_BREAKUP, ['Fortere']] in rules
