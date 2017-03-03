import math, re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *
from hamplify.parsers.block import BlockParser
from hamplify.parsers.comment import CommentParser
from hamplify.parsers.doctype import DoctypeParser
from hamplify.parsers.tags import TagParser

# Supports CRLF and LF newlines
regex_newline = re.compile(r"\r?\n")

class Parser(BaseParser):
  def __init__(self, options=None):
    super(Parser, self).__init__(options)

    self.tag_parser = TagParser(options)
    self.block_parser = BlockParser(options)
    self.doctype_parser = DoctypeParser(options)
    self.comment_parser = CommentParser(options)

    self._reset()

  def _reset(self):
    self.ws_per_indent = None
    self.ws_char = None

    self.root = RootNode()
    self.cursor = self.root
    self.stack = [self.root]

  def parse(self, text):
    """ Parses a block of HAML and returns an element tree
    """

    self._reset()
    text = regex_newline.split(text)
    line_number = 0
    line = None

    try:
      for line in text:
        indentation = self._get_indentation(line)
        line = line.lstrip()
        line_number += 1

        # If the line has indentation, then it cannot be blank/whitespace
        if indentation is not None:
          level = self._block_level()

          # Comments can span multiple lines, so make sure we don't parse them
          if self._in_comment(indentation):
            self._push(Text(line))
            continue

          # Pop elements off the stack based on how the indentation changed
          if indentation < level:
            while indentation < level and level > 0:
              self._pop()
              level -= 1
          elif indentation > level:
            raise ParseError("Too much indentation (%d indents too many)" % (indentation - level))

          element = self._parse_line(line)
          self._push(element)
        else:
          self._push(Text())
    except ParseError as pe:
      pe.line_number = line_number
      pe.line = line
      raise pe

    return self.root

  def _parse_line(self, line):
    """ Checks if the line starts with any tokens that designate a tag
    or block, and parses it if it does. Otherwise returns a text object
    """

    for t in COMMENT_TOKENS:
      if line.startswith(t):
        return self.comment_parser.parse(line)

    for t in TAG_TOKENS:
      if line.startswith(t):
        return self.tag_parser.parse(line)

    if self.options.get("engine") and line.startswith(TOKEN_BLOCK):
      block = self.block_parser.parse(line, self._get_newest_child())
      return block 

    if line.startswith(TOKEN_DOCTYPE):
      return self.doctype_parser.parse(line)

    return Text(line)

  def _push(self, element):
    """ Adds the element to the current element under the cursor, and pushes the
    element onto the stack if the element is a node (i.e. it can have children)
    """

    self.cursor.add_child(element)

    # The stack is only so we can establish a parent/child hierarchy.
    # Elements which can't have children don't belong on the stack
    if isinstance(element, Node):
      self.stack.append(element)
      self.cursor = element

  def _pop(self):
    """ Removes the element at the top of the stack and returns it
    """

    if len(self.stack) == 1:
      raise Exception("Tried to pop stack while it was empty")

    e = self.stack.pop()
    self.cursor = self.stack[-1]

    return e

  def _block_level(self):
    """ Gets the current depth of the parser. 
    """

    return len(self.stack) - 1

  def _get_indentation(self, line):
    """ Calculates the indentation level of the line
    """

    last = None

    for i in range(len(line)):
      c = line[i]

      if c not in INDENTATION:
        if not self.ws_char:
          # This is not the first character in the line (i.e. the line has some indentation)
          if last:
            self.ws_char = last
            self.ws_per_indent = i

            # The first indentation is the first level
            return 1
          else:
            return 0
        else:
          indent = float(i) / self.ws_per_indent
          floored = math.floor(indent)

          # Indentation must be an even multiple of previous indentation, unless we're
          # inside a comment
          if floored < indent and not self._in_comment(floored):
            raise ParseError("Uneven indentation level (expected multiple of %d)" % self.ws_per_indent)

          return floored

      # The line starts with whitespace but does not match with what we expect
      # the whitespace to be
      elif self.ws_char and c != self.ws_char:
        raise ParseError("Mismatched whitespace at start of line (use spaces or tabs, not both)")

      last = c

    # This is a blank line (don't count indentation)
    return None

  def _in_comment(self, indentation=None):
    """ Returns true if the text at a given indentation would be captured
    as a comment
    """

    return indentation >= self._block_level() and type(self.cursor) is Comment

  def _get_newest_child(self):
    """ Returns the most recently added in child from the cursor, that isn't
    a blank text node. Returns None if no applicable node was found
    """

    for child in self.cursor.children[::-1]:
      if type(child) is Text and child.is_empty():
        continue
      else:
        return child

    return None