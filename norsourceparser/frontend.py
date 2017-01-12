import sys

from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.parsing.parser import Parser as TParser
import xml.etree.ElementTree as ET

"""
This file contains a simple front-end entrypoint to use to convert files.
"""

expected_usage = """
Expected usage: python frontend.py <pos|standard> <inputfile> <outputfile>
"""


def parse_standard(file_in, file_out):
    tc_parse_result = Parser().parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


def parse_pos(file_in, file_out):
    tc_parse_result = PosTreeParser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


def main():
    if len(sys.argv) < 3:
        print(expected_usage)
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]

        if arg1 == "pos":
            parse_pos(arg2, arg3)
        else:
            parse_standard(arg2, arg3)

