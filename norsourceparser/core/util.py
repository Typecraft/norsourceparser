import os
import json


lex_fp = open(os.path.join(os.path.dirname(__file__), '../resources/lex.json'), 'r')
inflections_fp = open(os.path.join(os.path.dirname(__file__), '../resources/inflections.json'), 'r')
lex = json.load(lex_fp)
inflections = json.load(inflections_fp)

lex_fp.close()
inflections_fp.close()


def parse_lexical_entry_rule(name):
    stem = pos = gloss = None
    name = name.split("_")

    if len(name) > 0:
        stem = name[0]

    if len(name) > 1:
        pos = name[1]

    if len(name) > 2:
        gloss = name[2]

    return [stem, pos, gloss]
