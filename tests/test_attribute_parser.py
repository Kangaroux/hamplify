import unittest

from hamplify.element import *
from hamplify.parser import *

class TestAttributeParser(unittest.TestCase):
  def test_plaintext(self):
    ap = AttributeParser()

    self.assertEquals(ap.parse('(class="test" required)'),
      ({
        "class": "test",
        "required": None
      }, ""))