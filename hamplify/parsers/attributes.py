from collections import OrderedDict

from .base import BaseParser
from hamplify.config import *

class Attribute():
  name = None
  value = None

  # The quote character that wraps the attributes (single/double)
  quote_char = ""

  def __eq__(self, other):
    """ Required for unit tests to be able to compare this to a regular dict
    with regular types for values
    """

    if type(other) is Attribute:
      return other == self
    else:
      return other == self.value

  def render(self):
    if self.value is None:
      return self.name
    elif type(self.value) is int:
      return "%s=%d" % (self.name, self.value)
    else:
      return "%s=%s%s%s" % (self.name, self.quote_char, self.value, self.quote_char)

class AttributeParser(BaseParser):
  """ State-based parser for extracting attributes from a tag.
  """

  STATE_DONE = 0
  STATE_PRE_NAME_WS = 1
  STATE_ATTR_NAME = 2
  STATE_POST_NAME_WS = 3
  STATE_PRE_VALUE_WS = 4
  STATE_VALUE = 5

  def __init__(self, options=None):
    super(AttributeParser, self).__init__(options)

    self._reset()

  def _reset(self):
    self.attrs = OrderedDict()
    self.cur_attr = Attribute()
    self.buffer = ""
    self.char = None
    self.pos = 0
    self.state = self.STATE_PRE_NAME_WS
    self.value_type = str
    self.quote_char = None

  def parse(self, text):
    """ Parses an attribute string, returning a 2-tuple of the attributes as a dictionary,
    and whatever text was remaining after the attributes.

    e.g. parse('(type="text" required)')

    returns ({"type": "text", "required": None}, "")
    """

    # Reset the parser state
    self._reset()

    self.length = len(text)
    self.char = text[self.pos]

    # This parser expects to the string to start right at the attributes
    if self.char != TOKEN_ATTR_WRAPPER[0]:
      raise ParseError("Expected a space or '%s', but found '%s' instead." % (TOKEN_ATTR_WRAPPER[0], self.char))

    self.pos += 1

    # Iterate through each character, changing states as we progress
    while self.state != self.STATE_DONE and self.pos < self.length:
      self.char = text[self.pos]

      if self.state == self.STATE_PRE_NAME_WS:
        self._parse_pre_name_whitespace()
      elif self.state == self.STATE_ATTR_NAME:
        self._parse_attr_name()
      elif self.state == self.STATE_POST_NAME_WS:
        self._parse_post_name_whitespace()
      elif self.state == self.STATE_PRE_VALUE_WS:
        self._parse_pre_value_whitespace()
      elif self.state == self.STATE_VALUE:
        self._parse_value()

      self.pos += 1

    if self.state != self.STATE_DONE:
      raise ParseError("Reached EOL while parsing attributes")

    return (self.attrs, text[self.pos:].lstrip())

  def push_attr(self):
    """ Adds a new attribute to the dictionary. If this is called before a value is
    set, the value will be None
    """

    val = None

    # The attribute has already been set
    if self.cur_attr.name in self.attrs:
      raise ParseError("Found duplicate attribute: %s" % self.cur_attr.name)

    if self.cur_attr.value is not None:
      self.cur_attr.value = self.value_type(self.cur_attr.value)

    self.attrs[self.cur_attr.name] = self.cur_attr
    self.cur_attr = Attribute()
    self.quote_char = None
    self.value_type = str
    self.buffer = ""

  def _parse_pre_name_whitespace(self):
    """ Skip whitespace and change states once we hit some characters that 
    could be for an attribute name

     vv        v
    (  href="#" target="_blank")
    """

    if self.char == " ":
      return

    if 'a' <= self.char.lower() <= 'z' or self.char == "-":
      self.state = self.STATE_ATTR_NAME
      self.buffer += self.char
    elif self.char == TOKEN_ATTR_WRAPPER[1]:
      self.state = self.STATE_DONE
    else:
      raise ParseError("Unexpected character while parsing attribute name: '%s'" % self.char)

  def _parse_attr_name(self):
    """ Parses an attribute name, building up the buffer as it reads in characters.
    Once a non-attribute character is hit, the buffer is dumped into attr_name.
    """

    if 'a' <= self.char.lower() <= 'z' or self.char == "-":
      self.buffer += self.char
    else:
      self.cur_attr.name = self.buffer

      if self.char == " ":
        self.state = self.STATE_POST_NAME_WS
      elif self.char == TOKEN_ATTR_SETVAL:
        self.state = self.STATE_PRE_VALUE_WS
        self.buffer = ""
      elif self.char == TOKEN_ATTR_WRAPPER[1]:
        self.state = self.STATE_DONE
        self.push_attr()
      else:
        raise ParseError("Unexpected character while parsing attribute name: '%s'" % self.char)

  def _parse_post_name_whitespace(self):
    """ Skips whitespace after the attribute name until:

    - An equal sign is found (which means this attribute has a value)
    - Attribute chars are found (which means no value, and another attribute)
    """

    if self.char == " ":
      return

    if 'a' <= self.char.lower() <= 'z' or self.char == "-":
      self.push_attr()
      self.state = self.STATE_ATTR_NAME
      self.buffer += self.char
    elif self.char == TOKEN_ATTR_SETVAL:
      self.state = self.STATE_PRE_VALUE_WS
      self.buffer = ""
    elif self.char == TOKEN_ATTR_WRAPPER[1]:
      self.state = self.STATE_DONE
      self.push_attr()
    else:
      raise ParseError("Unexpected character while parsing: '%s'" % self.char)

  def _parse_pre_value_whitespace(self):
    """ Skips whitespace before a value. If a character or quote is encountered, then the
    value is set to be a string. Otherwise the value is set to be an int
    """

    if self.char == " ":
      return

    if self.char == "\"":
      self.cur_attr.quote_char = "\""
      self.quote_char = "\""
      self.state = self.STATE_VALUE
    elif self.char == "\'":
      self.cur_attr.quote_char = "\'"
      self.quote_char = "\'"
      self.state = self.STATE_VALUE
    elif '0' <= self.char <= '9':
      self.value_type = int
      self.buffer += self.char
      self.state = self.STATE_VALUE
    elif self.char == TOKEN_ATTR_WRAPPER[1]:
      raise ParseError("Unexpected end of attributes (do you have an extra equals sign?)")
    else:
      raise ParseError("Unexpected character while parsing: '%s'" % self.char)

  def _parse_value(self):
    """ Parses the attribute's value. If the value is wrapped in quotes, extract
    every character until we hit the closing quote. If it's a number, extract values
    until we hit a space/other boundary
    """

    # If we hit the other quote char, or there was no quote char and we just hit some whitespace
    if self.char == self.quote_char or self.char == " " and not self.quote_char:
      self.state = self.STATE_PRE_NAME_WS
      self.cur_attr.value = self.buffer
      self.push_attr()
    elif not self.quote_char and self.char == TOKEN_ATTR_WRAPPER[1]:
      self.state = self.STATE_DONE
      self.cur_attr.value = self.buffer
      self.push_attr()
    elif not ('0' <= self.char <= '9') and self.value_type == int:
      raise ParseError("String attributes must be surrounded with quotes")
    else:
      self.buffer += self.char