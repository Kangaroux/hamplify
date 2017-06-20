import unittest

from hamplify.element import *
from hamplify.config import *
from hamplify.parsers.variable import VariableParser

class TestVariableParser(unittest.TestCase):
  vp = None

  def setUp(self):
    self.vp = VariableParser({"engine": ENGINE_DJANGO})

  def test_variable(self):
    e = self.vp.parse("= my.var")
    assert e.render() == "{{my.var}}"

  def test_variable_with_filters(self):
    e = self.vp.parse("= my.var | truncatechars|length ")
    assert e.render() == "{{my.var | truncatechars|length}}"

  def test_blank_variable(self):
    with self.assertRaises(ParseError):
      self.vp.parse("= ")

  def test_no_engine_set(self):
    self.vp = VariableParser()
    with self.assertRaises(ParseError):
      self.vp.parse("= variable")