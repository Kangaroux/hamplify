import unittest

from hamplify.element import *
from hamplify.config import ParseError
from hamplify.parsers.filter import FilterParser

class TestCommentParser(unittest.TestCase):
  fp = FilterParser()

  def test_plaintext(self):
    e = self.fp.parse("some plaintext")
    assert type(e) is Text

  def test_plain_filter(self):
    self.assertIsInstance(self.fp.parse(":plain"), FilterPlain)

  def test_javascript_filter(self):
    self.assertIsInstance(self.fp.parse(":javascript"), FilterJavascript)

  def test_css_filter(self):
    self.assertIsInstance(self.fp.parse(":css"), FilterCSS)