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
    assert e.id == None
    assert e.children == []

  def test_bad_class(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%button.[class]")

  def test_class(self):
    e = self.lp.parse("%input.my_Class")
    assert e.classes == ["my_Class"]

    e = self.lp.parse(".class(class='another')")
    assert e.render() == '<div class="another class"></div>'

    with self.assertRaises(ParseError):
      e = self.lp.parse(".#id")

    with self.assertRaises(ParseError):
      self.lp.parse("%input#")

  def test_multiple_classes(self):
    e = self.lp.parse("%input.class1.class2.class3")
    assert e.classes == ["class1", "class2", "class3"]

  def test_bad_id(self):
    with self.assertRaises(ParseError):
      self.lp.parse("%button#id/")

  def test_id(self):
    e = self.lp.parse("%input#id-")
    assert e.id == "id-"

    # Unsure how to deal with a tag that has more than 1 ID
    with self.assertRaises(ParseError):
      self.lp.parse("#id(id='another-id')").render()

  def test_remainder(self):
    e = self.lp.parse("%input some text")
    assert len(e.children) == 1
    assert e.children[0].text == "some text"

  def test_no_tag_name(self):
    e = self.lp.parse(".class#id some text")
    assert e.classes == ["class"]
    assert e.id == "id"
    assert e.children[0].text == "some text"

    e = self.lp.parse("#test")
    assert e.id == "test"

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

  def test_render(self):
    assert (self.lp.parse("%a.class#id(href='#'  data-blah=1234 required )").render()
      == '<a id="id" class="class" href="#" data-blah=1234 required></a>')