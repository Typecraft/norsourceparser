import sys
import click

from norsourceparser.core.config import config
from norsourceparser.core.parser import Parser, PosTreeParser
from typecraft_python.parsing.parser import Parser as TParser


def parse_standard(file_in, file_out):
    tc_parse_result = Parser.parse_file(file_in)
    TParser.write_to_file(file_out, tc_parse_result)


def parse_pos(file_in, file_out):
    tc_parse_result = PosTreeParser.parse_file(file_in)
    TParser.write_to_file(file_out, [tc_parse_result])


@click.command()
@click.option('--debug/--no-debug', default=False, help='Enables debug mode. Will print errors')
@click.option('--mode', default='standard', type=click.Choice(['standard', 'pos']))
@click.option('--max-phrases-per-text', type=int, default=-1)
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def main(
    debug,
    mode,
    max_phrases_per_text,
    input,
    output
):
    """
    Main entry point for the parser.

    The entry point accepts 2-3 arguments, type, input and output respectively.
    :return: void
    """
    config.DEBUG = debug or False
    config.MAX_PHRASES_PER_TEXT = max_phrases_per_text

    if mode == 'standard':
        parse_standard(input, output)
    elif mode == 'pos':
        parse_pos(input, output)
