# coding=utf-8
from __future__ import unicode_literals
from norsourceparser.core.constants import REDUCED_RULE_POS, REDUCED_RULE_MORPHOLOGICAL_BREAKUP, REDUCED_RULE_GLOSSES
from norsourceparser.core.models import SyntaxNode
from norsourceparser.core.rules import parse_lexical_entry


def test_parse_lexical_entry_with_typical_input():
    rules = parse_lexical_entry(SyntaxNode(name='løper'), 'løpe', 'V', None)

    assert len(rules) == 3


def test_parse_lexical_entry_with_terminal_equal_to_stem():
    rules = parse_lexical_entry(SyntaxNode(name='løpe'), 'løpe', 'V', None)

    assert len(rules) == 3


def test_parse_lexical_entry_with_gloss():
    rules = parse_lexical_entry(SyntaxNode(name='Hunden'), 'Hunden', 'N', 'SG.DEF.MASC')

    assert len(rules) == 4


def test_parse_lexical_entry_non_NVADJ_returns_breakup():
    rules = parse_lexical_entry(SyntaxNode(name='Fortere'), 'Fortere', 'ADV', None)

    assert len(rules) == 2
