import unittest

from hamplify.element import *
from hamplify.config import ParseError
from hamplify.parsers.comment import CommentParser

class TestCommentParser(unittest.TestCase):
  cp = CommentParser()

  def test_plaintext(self):
    e = self.cp.parse("some plaintext")
    assert type(e) is Text

  def test_html_comment(self):
    self.assertIsInstance(self.cp.parse("-#"), Comment)

    e = self.cp.parse("-# A comment  ")
    assert " A comment  " == e.children[0].text
    assert "<!-- A comment   -->" == e.render()

  def test_comment(self):
    self.assertIsInstance(self.cp.parse("/"), Comment)

    e = self.cp.parse("/ %element.class")
    assert " %element.class" == e.children[0].text
    assert "" == e.render()

  def test_conditional_comment(self):
    self.assertIsInstance(self.cp.parse("-#[condition]"), ConditionalComment)

    e = self.cp.parse("-#[if IE]")
    assert e.condition == "if IE"