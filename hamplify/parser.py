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

def parse_line(text):
  # Collect whitespace from the beginning of the line
  whitespace = regex_whitespace.match(text)

  if whitespace:
    whitespace = whitespace.group(1)
    text = text[len(whitespace):]

  text = text.rstrip()

  if text:
    if text[0] == TOKEN_TAG:
      return parse_tag(text)
    elif text[0] == TOKEN_CLASS:
      print("div with class")
    elif text[0] == TOKEN_ID:
      print("div with id")
  
  # Empty/plaintext line
  return Text(text)

def parse_tag(text):
  tag = None
  tag_name = None

  # Remove the % tag
  text = text[1:]

  if not text:
    raise ParseError("Encountered a blank tag, expected a name")

  tag_name = regex_letters.match(text)

  if not tag_name:
    raise ParseError("Expected a name for the tag, but instead found %s" % text[0])

  tag_name = tag_name.group(1)

  tag = Tag(tag_name)
  text = text[len(tag_name):]

  if not text:
    return tag

  # Search for classes and ID. Both are optional, but they must come in the order
  # .class -> #id
  while text[0] == TOKEN_CLASS:
    class_name = regex_class_id.match(text)

    if not class_name:
      raise ParseError("Encountered an empty class name")

    class_name = class_name.group(1)

    tag.classes.append(class_name)
    text = text[len(class_name)+1:]

    if not text:
      return tag

  while text[0] == TOKEN_ID:
    # An ID was already set
    if tag.id:
      raise ParseError("Element has more than 1 ID")

    id_name = regex_class_id.match(text)

    if not id_name:
      raise ParseError("Encountered an empty ID")

    id_name = id_name.group(1)

    tag.id = id_name
    text = text[len(id_name)+1:]

    if not text:
      return tag

  if text[0] == TOKEN_CLASS:
    raise ParseError("Encountered a class after an ID (ID must be last)")
  elif text[0] != " ":
    raise ParseError("Expected a space, but found '%s' instead." % text[0])

  text = text[1:].lstrip()

  # There's some text leftover
  if not regex_whitespace.fullmatch(text):
    tag.add_child(Text(text))

  return tag