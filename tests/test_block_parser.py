import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.block import BlockParser

class TestBlockParser(unittest.TestCase):
  bp = BlockParser()

  def test_html_comment(self):
    self.assertIsInstance(self.bp.parse("-#"), Comment)

    e = self.bp.parse("-# A comment")
    assert " A comment" == e.children[0].text
    assert "<!-- A comment -->" == e.render()

  def test_comment(self):
    self.assertIsInstance(self.bp.parse("/"), Comment)

    e = self.bp.parse("/ %element.class")
    assert " %element.class" == e.children[0].text
    assert "" == e.render()

  def test_block(self):
    with self.assertRaises(ParseError):
      self.bp.parse("- ")

    block = self.bp.parse("-include")
    assert block.name == "include"
    assert block.args == ""

    block = self.bp.parse("- for x in list")
    assert block.name == "for"
    assert block.args == "x in list"