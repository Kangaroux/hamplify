import unittest

from hamplify.element import *
from hamplify.config import *
from hamplify.parsers.block import BlockParser

class TestBlockParser(unittest.TestCase):
  bp = BlockParser()

  def setUp(self):
    self.bp.options = {}

  def test_blocks_while_not_enabled(self):
    with self.assertRaises(ParseError):
      self.bp.parse("- block")

  def test_self_closing_blocks(self):
    self.bp.options["engine"] = ENGINE_JINJA

    block = self.bp.parse('-include "template.html"')
    assert type(block) is InlineBlock
    assert block.name == "include"
    assert block.args == '"template.html"'
    assert block.render() == '{% include "template.html" %}'

    self.bp.options["engine"] = ENGINE_DJANGO

    block = self.bp.parse("- for x in list")
    assert type(block) is Block
    assert block.name == "for"
    assert block.args == "x in list"
    assert block._pre_render() == "{% for x in list %}"
    assert block._post_render() == "{% endfor %}"

  def test_empty_block(self):
    self.bp.options["engine"] = ENGINE_DJANGO

    with self.assertRaises(ParseError):
      self.bp.parse("- ")