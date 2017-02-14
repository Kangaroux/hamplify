import unittest

from hamplify.element import *
from hamplify.parser import *

class TestParser(unittest.TestCase):
  def test_parse_plaintext(self):
    e = parse_line("      ")
    assert type(e) is Text
    assert e.text == ""

    e = parse_line("     some Plain text.!@#$%^&*()")
    assert type(e) is Text
    assert e.text == "some Plain text.!@#$%^&*()"

  def test_parse_tag(self):
    with self.assertRaises(ParseError):
      parse_tag("%")

    with self.assertRaises(ParseError):
      parse_tag("% sometext")

    e = parse_tag("%button")
    assert e.tag == "button"
    assert e.classes == []
    assert e.id == ""
    assert e.children == []

    e = parse_tag("%input.my_Class")
    assert e.classes == ["my_Class"]

    e = parse_tag("%input.class1.class2.class3")
    assert e.classes == ["class1", "class2", "class3"]

    e = parse_tag("%input.class#id-")
    assert e.classes == ["class"]
    assert e.id == "id-"

    with self.assertRaises(ParseError):
      parse_tag("%input.class#id/")

    e = parse_tag("%input.class#id some text")
    assert len(e.children) == 1
    assert e.children[0].text == "some text"