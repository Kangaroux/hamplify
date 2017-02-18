import re

from .element import Tag, Text

regex_whitespace = re.compile(r'([ \t]+)')
regex_letters = re.compile(r'([a-zA-Z]+)')
regex_class_id = re.compile(r'(?:\.|#)([a-zA-Z0-9_-]*)')

TOKEN_TAG = "%"
TOKEN_CLASS = "."
TOKEN_ID = "#"
TOKEN_ATTR = ("(", ")")

class ParseError(Exception):
  pass

class LineParser:
  tag = None
  text = ""
  whitespace = ""

  def parse(self, text):
    """ Parses a single line of text, and produces either a Tag or Text element.

    This will remove leading/trailing whitespace.
    """

    self.tag = Tag()
    self.text = text.rstrip()
    self._collect_whitespace()

    if text:
      if text[0] == TOKEN_TAG:
        return self._parse()
      elif text[0] == TOKEN_CLASS:
        print("div with class")
      elif text[0] == TOKEN_ID:
        print("div with id")

    # Plaintext or blank line
    return Text(self.text)

  def _collect_whitespace(self):
    """ Removes any leading whitespace from the text and stores it
    """

    ws = regex_whitespace.match(self.text)

    if ws:
      ws = ws.group(1)
      self.text = self.text[len(ws):]

    self.whitespace = ws

  def _parse(self):
    """ Parses a tag and any immediate text contents.

    %p.style#id Lorem ipsum

    Produces: <p class="style" id="id">Lorem ipsum</p>
    """

    self._parse_tag_name()
    self._parse_classes()
    self._parse_id()

    if self.text:
      self._parse_attributes()
      self._parse_remainder()

    return self.tag

  def _parse_tag_name(self):
    """ Extracts the tag name and strips it from the text.

    [%p].style#id
    """

    # Remove the %
    self.text = self.text[1:]

    if not self.text:
      raise ParseError("Encountered a blank tag, expected a name")

    tag_name = regex_letters.match(self.text)

    if not tag_name:
      raise ParseError("Expected a name for the tag, but instead found %s" % self.text[0])

    tag_name = tag_name.group(1)

    self.tag.tag = tag_name
    self.text = self.text[len(tag_name):]

  def _parse_classes(self):
    """ Extracts a list of classes (if any)

    %p[.style]#id
    """

    while self.text and self.text[0] == TOKEN_CLASS:
      class_name = regex_class_id.match(self.text)

      if not class_name:
        raise ParseError("Encountered an empty class name")

      class_name = class_name.group(1)

      self.tag.classes.append(class_name)
      self.text = self.text[len(class_name)+1:]

  def _parse_id(self):
    """ Extracts an ID for the element (if it has one)

    %p.style[#id]
    """

    while self.text and self.text[0] == TOKEN_ID:
      # An ID was already set
      if self.tag.id:
        raise ParseError("Element cannot have more than 1 ID")

      id_name = regex_class_id.match(self.text)

      if not id_name:
        raise ParseError("Encountered an empty ID")

      id_name = id_name.group(1)

      self.tag.id = id_name
      self.text = self.text[len(id_name)+1:]

    if self.text and self.text[0] == TOKEN_CLASS:
      raise ParseError("Encountered a class after an ID (ID must be last)")

  def _parse_attributes(self):
    """ Extracts attributes as a dictionary

    %a(href="#" target="_blank")
    => {
      "href": "#",
      "target": "_blank"
    }
    """

    # A space means no attributes
    if self.text[0] == " ":
      return
    
    if self.text[0] != TOKEN_ATTR[0]:
      raise ParseError("Expected a space or '%s', but found '%s' instead." % (TOKEN_ATTR[0], self.text[0]))

    STATE_WHITESPACE = 0
    STATE_NAME = 1
    STATE_VALUE = 2

    """

    Initial state: SKIP_WHITESPACE
    reach a letter: STATE_NAME
    store chars as attribute name

    (optional)
    reach white space: SKIP_WHITESPACE
    OR reach equal sign: SKIP_WHITESPACE, set flag saying we expect a value



    """

    try:
      # Current character
      c = None

      # Previous character
      last = None

      attr_name = ""
      attr_val = ""

      scanning_val = False

      i = 0
      while True:
        i += 1

        last = c
        c = self.text[i]

        # Skip whitespace
        if c == " " and not scanning_val:
          continue

        if not scanning_val:
          if c == "=":
            continue

    except IndexError:
      raise ParseError("Unexpected EOL while reading attributes.")


  def _parse_remainder(self):
    """ Parses any plain text that may come after the element

    %p.style#id [Lorem ipsum]
    """

    self.text = self.text[1:].lstrip()

    if self.text:
      self.tag.add_child(Text(self.text))

class AttributeParser:
  STATE_DONE = 0
  STATE_PRE_NAME_WS = 1
  STATE_ATTR_NAME = 2
  STATE_POST_NAME_WS = 3
  STATE_PRE_VALUE_WS = 4
  STATE_VALUE = 5

  def _reset(self):
    self.attrs = {}
    self.attr_name = None
    self.attr_value = None
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

    returns ({"type": "text", "required": "None"}, "")
    """

    # Reset the parser state
    self._reset()

    self.length = len(text)
    self.char = text[self.pos]

    # This parser expects to the string to start right at the attributes
    if self.char != TOKEN_ATTR[0]:
      raise ParseError("Expected a space or '%s', but found '%s' instead." % (TOKEN_ATTR[0], self.char))

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

    if self.attr_value is not None:
      val = self.value_type(self.attr_value)

    self.attrs[self.attr_name] = val
    self.attr_name = None
    self.attr_value = None
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
    elif self.char == TOKEN_ATTR[1]:
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
      self.attr_name = self.buffer

      if self.char == " ":
        self.state = self.STATE_POST_NAME_WS
      elif self.char == "=":
        self.state = self.STATE_PRE_VALUE_WS
        self.buffer = ""
      elif self.char == TOKEN_ATTR[1]:
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
    elif self.char == "=":
      self.state = self.STATE_PRE_VALUE_WS
      self.buffer = ""
    elif self.char == TOKEN_ATTR[1]:
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
      self.quote_char = "\""
      self.state = self.STATE_VALUE
    elif self.char == "\'":
      self.quote_char = "\'"
      self.state = self.STATE_VALUE
    elif '0' <= self.char <= '9':
      self.value_type = int
      self.buffer += self.char
      self.state = self.STATE_VALUE
    elif self.char == TOKEN_ATTR[1]:
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
      self.attr_value = self.buffer
      self.push_attr()
    elif not self.quote_char and self.char == TOKEN_ATTR[1]:
      self.state = self.STATE_DONE
      self.attr_value = self.buffer
      self.push_attr()
    elif not ('0' <= self.char <= '9') and self.value_type == int:
      raise ParseError("String attributes must be surrounded with quotes")
    else:
      self.buffer += self.char