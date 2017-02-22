import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.block import BlockParser

class TestBlockparser(unittest.TestCase):
  bp = BlockParser()

  def test_html_comment(self):
    self.assertIsInstance(self.bp.parse("-#"), Comment)
    assert " A comment" == self.bp.parse("-# A comment").children[0].text

  def test_comment(self):
    self.assertIsInstance(self.bp.parse("/"), Comment)
    assert " %element.class" == self.bp.parse("/ %element.class").children[0].text

  def test_block(self):
    block = self.bp.parse("-include")
    assert block.name == "include"
    assert block.args == ""

    block = self.bp.parse("- for x in list")
    assert block.name == "for"
    assert block.args == "x in list"