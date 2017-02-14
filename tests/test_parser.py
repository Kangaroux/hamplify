import unittest

from hamplify.element import *
from hamplify.parser import *

class TestParser(unittest.TestCase):
  lp = LineParser()

  def test_plaintext(self):
    e = self.lp.parse("      ")
    assert type(e) is Text
    assert e.text == ""

    e = self.lp.parse("     some Plain text.!@#$%^&*()")
    assert e.text == "some Plain text.!@#$%^&*()"

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