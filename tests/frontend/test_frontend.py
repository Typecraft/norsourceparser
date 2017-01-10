import re
import pytest

file_1 = __file__
print(__file__)


def test_load():
    assert file_1 is not None


