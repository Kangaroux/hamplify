import unittest

from hamplify.element import *
from hamplify.parsers.attributes import AttributeParser
from hamplify.parsers.config import ParseError

class TestAttributeParser(unittest.TestCase):
  ap = AttributeParser()

  def test_nothing(self):
    self.assertEquals(self.ap.parse('()'),
      ({}, ""))

  def test_whitespace(self):
    self.assertEquals(self.ap.parse('(   )'),
      ({}, ""))

    self.assertEquals(self.ap.parse('( href  = \'#\' )'),
      ({
        "href": "#"
      }, ""))

  def test_string_values(self):
    self.assertEquals(self.ap.parse('(href="#")'),
      ({
        "href": "#"
      }, ""))

    self.assertEquals(self.ap.parse('(class="someClass Another-class")'),
      ({
        "class": "someClass Another-class"
      }, ""))

    self.assertEquals(self.ap.parse('(title="This title has \'some\' quotes")'),
      ({
        "title": "This title has 'some' quotes"
      }, ""))

  def test_int_values(self):
    self.assertEquals(self.ap.parse('(rows=5)'),
      ({
        "rows": 5
      }, ""))

  def test_no_value(self):
    self.assertEquals(self.ap.parse('(readonly)'),
      ({
        "readonly": None
      }, ""))

    self.assertEquals(self.ap.parse('(required autocomplete )'),
      ({
        "required": None,
        "autocomplete": None
      }, ""))

    self.assertEquals(self.ap.parse('(href="#" required)'),
      ({
        "required": None,
        "href": "#"
      }, ""))

  def test_text_after_attributes(self):
    self.assertEquals(self.ap.parse('(attr="value") some text'),
      ({
        "attr": "value"
      }, "some text"))

  def test_errors(self):
    with self.assertRaises(ParseError):
      self.ap.parse('not attributes')

    with self.assertRaises(ParseError):
      self.ap.parse('(href="#" =123)')

    with self.assertRaises(ParseError):
      self.ap.parse('(target=_blank)')

    with self.assertRaises(ParseError):
      self.ap.parse('(name$=123)')

    with self.assertRaises(ParseError):
      self.ap.parse('(rows=5a)')

    with self.assertRaises(ParseError):
      self.ap.parse('(incomplete')

    with self.assertRaises(ParseError):
      self.ap.parse('(incomplete=)')

    with self.assertRaises(ParseError):
      self.ap.parse('(incomplete ^)')

    with self.assertRaises(ParseError):
      self.ap.parse('(incomplete="test)')