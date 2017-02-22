import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.parser import Parser

class TestFullParser(unittest.TestCase):
  p = Parser()

  def test_single_line_indentation(self):
    self.p._reset()
    assert 0 == self.p._get_indentation("")

    self.p._reset()
    assert 0 == self.p._get_indentation("  ")

    self.p._reset()
    assert 0 == self.p._get_indentation("text")

    self.p._reset()
    assert 1 == self.p._get_indentation("  text")
    assert self.p.ws_per_indent == 2
    assert self.p.ws_char == " "

  def test_indentation(self):
    self.p._reset()
    assert 0 == self.p._get_indentation("some text")
    assert 1 == self.p._get_indentation("  Indented")
    assert 2 == self.p._get_indentation("    Some more")
    assert 0 == self.p._get_indentation("")
    assert 1 == self.p._get_indentation("  Back down")

  def test_mixed_indentation(self):
    self.p._reset()
    self.p.ws_per_indent = 2
    self.p.ws_char = " "

    with self.assertRaises(ParseError):
      self.p._get_indentation("\tTabs")

    with self.assertRaises(ParseError):
      self.p._get_indentation("\t  Mixed")

    with self.assertRaises(ParseError):
      self.p._get_indentation("  \tMixed")

  def test_uneven_indentation(self):
    self.p._reset()
    self.p.ws_per_indent = 4
    self.p.ws_char = " "

    with self.assertRaises(ParseError):
      self.p._get_indentation("  2 spaces instead of 4")

  def test_multiline(self):
    self.p._reset()

    html = self.p.parse("""
%html
  %head
    %title My cool title
  %body
    .container
      %p some text
      """).render()

    assert (html == "<html><head><title>My cool title</title></head><body>"
      "<div class=\"container\"><p>some text</p></div></body></html>")