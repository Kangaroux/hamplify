import unittest

from hamplify.element import *
from hamplify.parsers.config import ParseError
from hamplify.parsers.doctype import DoctypeParser

class TestDoctypeParser(unittest.TestCase):
  dtp = DoctypeParser()

  def test_common_doctypes(self):
    assert self.dtp.parse("!!! ").text == '<!DOCTYPE html>'
    assert self.dtp.parse("!!! 5").text == '<!DOCTYPE html>'
    assert self.dtp.parse("!!! 1.0").text == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
    assert self.dtp.parse("!!! StrICT").text == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'

  def test_bad_doctypes(self):
    with self.assertRaises(ParseError):
      self.dtp.parse("!!!!")
      self.dtp.parse("!!! 4")