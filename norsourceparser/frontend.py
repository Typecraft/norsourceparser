import sys

from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.parsing.parser import Parser as TParser
import xml.etree.ElementTree as ET

"""
This file contains a simple front-end entrypoint to use to convert files.
"""

expected_usage = """
Expected usage: python frontend.py <pos|standard(DEFAULT)>? <inputfile> <outputfile>
"""


def parse_standard(file_in, file_out):
    tc_parse_result = Parser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


def parse_pos(file_in, file_out):
    tc_parse_result = PosTreeParser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


def main():
    """
    Main entrypoint for the parser.

    The entrypoint accepts 2-3 arguments, type, input and output respectively.
    :return: void
    """
    type, input, output = None, None, None
    if len(sys.argv) < 2:
        print(expected_usage)
        return
    if len(sys.argv) == 3:
        type = 'default'
        input, output = sys.argv[1:3]
    else:
        type, input, output = sys.argv[1:4]

    if type == "pos":
        parse_pos(input, output)
    else:
        parse_standard(input, output)

