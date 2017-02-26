import re

from .attributes import AttributeParser
from .base import BaseParser
from hamplify.config import *
from hamplify.element import SelfClosingTag, Tag, Text

regex_tag_name = re.compile(r'([a-zA-Z][a-zA-Z0-9]*)')
regex_class_id = re.compile(r'(?:\.|#)([a-zA-Z0-9_-]*)')

class TagParser(BaseParser):
  """ Regex parser for parsing out a %tag. 
  """

  def __init__(self, options=None):
    super(TagParser, self).__init__(options)

    self.ap = AttributeParser(options)
    self._reset()

  def _reset(self):
    self.tag = None
    self.text = None

  def parse(self, text):
    """ Parses a single line of text, and produces either a Tag or Text element.
    """

    self._reset()
    self.text = text

    if text:
      if text.startswith(TOKEN_TAG):
        return self._parse()
      elif text.startswith(TOKEN_CLASS) or text.startswith(TOKEN_ID):
        self.tag = Tag()
        self.tag.tag = "div"
        return self._parse(False)

    # Plaintext or blank line
    return Text(self.text)

  def _parse(self, parse_name=True):
    """ Parses a tag and any immediate text contents.

    %p.style#id Lorem ipsum

    Produces: <p class="style" id="id">Lorem ipsum</p>
    """

    if parse_name:
      self._parse_tag_name()
      
    self._parse_classes()
    self._parse_id()
    self._parse_attributes()

    return self.tag

  def _parse_tag_name(self):
    """ Extracts the tag name and strips it from the text.

    [%p].style#id
    """

    # Remove the tag token
    self.text = self.text[len(TOKEN_TAG):]

    if not self.text:
      raise ParseError("Encountered a blank tag, expected a name")

    tag_name = regex_tag_name.match(self.text)

    if not tag_name:
      raise ParseError("Expected a name for the tag, but instead found '%s'" % self.text[0])

    tag_name = tag_name.group(1)

    if tag_name.lower() in SELF_CLOSING_TAGS:
      self.tag = SelfClosingTag()
    else:
      self.tag = Tag()

    self.tag.tag = tag_name
    self.text = self.text[len(tag_name):]

  def _parse_classes(self):
    """ Extracts a list of classes (if any)

    %p[.style]#id
    """

    while self.text and self.text.startswith(TOKEN_CLASS):
      class_name = regex_class_id.match(self.text)
      class_name = class_name.group(1)

      if not class_name:
        raise ParseError("Encountered an empty class name")

      self.tag.classes.append(class_name)
      self.text = self.text[len(class_name)+1:]

  def _parse_id(self):
    """ Extracts an ID for the element (if it has one)

    %p.style[#id]
    """

    while self.text and self.text.startswith(TOKEN_ID):
      # An ID was already set
      if self.tag.id:
        raise ParseError("Element cannot have more than 1 ID")

      id_name = regex_class_id.match(self.text)
      id_name = id_name.group(1)

      if not id_name:
        raise ParseError("Encountered an empty ID")

      self.tag.id = id_name
      self.text = self.text[len(id_name) + len(TOKEN_ID):]

    if self.text and self.text.startswith(TOKEN_CLASS):
      raise ParseError("Encountered a class after an ID (ID must be last)")

  def _parse_attributes(self):
    if not self.text:
      return

    if self.text.startswith(TOKEN_ATTR_WRAPPER[0]):
      (attrs, text) = self.ap.parse(self.text)

      self.tag.attrs = attrs

      if text:
        self.tag.add_child(Text(text))
    elif self.text[0] == " ":
      self.tag.add_child(Text(self.text[1:]))
    else:
      raise ParseError("Expected a '%s' or whitespace" % TOKEN_ATTR_WRAPPER[0])