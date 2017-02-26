import unittest

from hamplify.element import *
from hamplify.config import ParseError

class TestElements(unittest.TestCase):
  """ None of these tests actually have any application, but it
  makes the code coverage look better ;)
  """

  def test_blank_element(self):
    assert Element().render() == ""

  def test_no_root_parent(self):
    with self.assertRaises(Exception):
      RootNode().set_parent(Node())