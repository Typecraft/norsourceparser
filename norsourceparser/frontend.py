import sys
import click

from norsourceparser.core.config import config
from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.parsing.parser import Parser as TParser


def parse_standard(file_in, file_out):
    tc_parse_result = Parser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


def parse_pos(file_in, file_out):
    tc_parse_result = PosTreeParser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


@click.command()
@click.option('--debug/--no-debug', default=False, help='Enables debug mode. Will print errors')
@click.option('--mode', default='standard', type=click.Choice(['standard', 'pos']))
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def main(debug, mode, input, output):
    """
    Main entrypoint for the parser.

    The entrypoint accepts 2-3 arguments, type, input and output respectively.
    :return: void
    """
    if debug:
        config.DEBUG = True
    if mode == 'standard':
        parse_standard(input, output)
    elif mode == 'pos':
        parse_pos(input, output)
