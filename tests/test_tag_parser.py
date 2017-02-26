import unittest

from hamplify.element import *
from hamplify.config import ParseError
from hamplify.parsers.tags import TagParser

class TestTagParser(unittest.TestCase):
  tp = TagParser()

  def test_plaintext(self):
    e = self.tp.parse("      ")
    assert type(e) is Text

  def test_bad_tag_name(self):
    with self.assertRaises(ParseError):
      self.tp.parse("%")

    with self.assertRaises(ParseError):
      self.tp.parse("% sometext")

  def test_tag_name(self):
    with self.assertRaises(ParseError):
      self.tp.parse("%input#id/")

    e = self.tp.parse("%button")
    assert type(e) is Tag
    assert e.tag == "button"
    assert e.classes == []
    assert e.id == None
    assert e.children == []

    e = self.tp.parse("%h1")
    assert e.tag == "h1"

  def test_class(self):
    e = self.tp.parse("%input.my_Class")
    assert e.classes == ["my_Class"]

    e = self.tp.parse(".class(class='another')")
    assert e.render() == '<div class="another class"></div>'

    with self.assertRaises(ParseError):
      e = self.tp.parse(".#id")

    with self.assertRaises(ParseError):
      self.tp.parse("%button.[class]")

    with self.assertRaises(ParseError):
      self.tp.parse("#id.class")

  def test_multiple_classes(self):
    e = self.tp.parse("%input.class1.class2.class3")
    assert e.classes == ["class1", "class2", "class3"]

  def test_id(self):
    e = self.tp.parse("%input#id-")
    assert e.id == "id-"

    with self.assertRaises(ParseError):
      self.tp.parse("%input#")

    # Unsure how to deal with a tag that has more than 1 ID
    with self.assertRaises(ParseError):
      self.tp.parse("#id(id='another-id')").render()

    with self.assertRaises(ParseError):
      self.tp.parse("#some-id#another-id")

    with self.assertRaises(ParseError):
      self.tp.parse("%button#id/")

  def test_remainder(self):
    e = self.tp.parse("%p some text")
    assert len(e.children) == 1
    assert e.children[0].text == "some text"

    e = self.tp.parse("%textarea   whitespace   ")
    assert e.children[0].text == "  whitespace   "

  def test_no_tag_name(self):
    e = self.tp.parse(".class#id some text")
    assert e.classes == ["class"]
    assert e.id == "id"
    assert e.children[0].text == "some text"

    e = self.tp.parse("#test")
    assert e.id == "test"

  def test_full_line(self):
    e = self.tp.parse('%a.class#id(href="#" target="_blank" required var=123) Some extra text!')
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
    assert (self.tp.parse("%a.class#id(href='#'  data-blah=1234 required )").render()
      == '<a id="id" class="class" href="#" data-blah=1234 required></a>')

  def test_self_closing_tag(self):
    e = self.tp.parse("%br")
    assert type(e) is SelfClosingTag
    assert e.render() == "<br />"

    e = self.tp.parse("%link(rel='stylesheet' href='blah.css')")
    assert e.render() == '<link rel="stylesheet" href="blah.css" />'