import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.tags import TagParser

class TestTagParser(unittest.TestCase):
  lp = TagParser()

  def test_plaintext(self):
    e = self.lp.parse("      ")
    assert type(e) is Text

  def test_bad_tag_name(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%")

    with self.assertRaises(ParseError):
      self.lp.parse("% sometext")

  def test_tag_name(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%input#id/")

    e = self.lp.parse("%button")
    assert type(e) is Tag
    assert e.tag == "button"
    assert e.classes == []
    assert e.id == ""
    assert e.children == []

  def test_bad_class(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%button.[class]")

  def test_class(self):
    e = self.lp.parse("%input.my_Class")
    assert e.classes == ["my_Class"]

  def test_multiple_classes(self):
    e = self.lp.parse("%input.class1.class2.class3")
    assert e.classes == ["class1", "class2", "class3"]

  def test_bad_id(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%button#id/")

  def test_id(self):
    e = self.lp.parse("%input#id-")
    assert e.id == "id-"    

  def test_remainder(self):
    e = self.lp.parse("%input some text")
    assert len(e.children) == 1
    assert e.children[0].text == "some text"

  def test_full_line(self):
    e = self.lp.parse('%a.class#id(href="#" target="_blank" required var=123) Some extra text!')
    assert e.tag == "a"
    assert e.classes == ["class"]
    assert e.id == "id"
    assert e.children[0].text == "Some extra text!"
    assert e.attrs == {
        "href": "#",
        "target": "_blank",
        "required": None,
        "var": 123
      }