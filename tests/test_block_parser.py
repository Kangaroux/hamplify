import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.block import BlockParser

class TestBlockParser(unittest.TestCase):
  bp = BlockParser()

  def test_block(self):
    with self.assertRaises(ParseError):
      self.bp.parse("- ")

    block = self.bp.parse("-include")
    assert block.name == "include"
    assert block.args == ""

    block = self.bp.parse("- for x in list")
    assert block.name == "for"
    assert block.args == "x in list"