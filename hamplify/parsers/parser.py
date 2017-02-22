import math, re

from .config import *
from hamplify.element import *
from hamplify.parsers.block import BlockParser
from hamplify.parsers.tags import TagParser

# Supports CRLF and LF newlines
regex_newline = re.compile(r"\r?\n")

class Parser:
  tag_parser = TagParser()
  block_parser = BlockParser()

  def _reset(self):
    self.ws_per_indent = None
    self.ws_char = None

    self.root = Node()
    self.cursor = self.root
    self.stack = [self.root]

  def parse(self, text):
    text = regex_newline.split(text)

    for line in text:
      print(line)
      indentation = self._get_indentation(line)
      line = line.lstrip()

      level = self._indent_level()

      # Indentation can only increase at a rate of once per line
      if indentation > (level + 1):
        raise ParseError("Indentation jumped too much (previous level was %d,"
          " now at %d)" % (level, indentation))
      elif indentation <= level:
        # If the indentation didn't increase, then some elements 
        # from the stack need to be popped
        while indentation <= level and level > 0:
          self._pop()
          level -= 1

      self._push(self._parse_line(line))

  def _parse_line(self, line):
    """ Checks if the line starts with any tokens that designate a tag
    or block, and parses it if it does. Otherwise returns a text object
    """

    for t in TAG_TOKENS:
      if line.startswith(t):
        return self.tag_parser.parse(line)

    for b in BLOCK_TOKENS:
      if line.startswith(b):
        return self.block_parser.parse(line)

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

    print(self._indent_level())

  def _pop(self):
    """ Removes the element at the top of the stack and returns it
    """

    if len(self.stack) == 1:
      raise Exception("Tried to pop stack while it was empty")

    e = self.stack.pop()
    self.cursor = self._top()

    return e

  def _top(self):
    """ Gets the top element on the stack
    """

    return self.stack[-1]

  def _indent_level(self):
    """ Gets the current indentation level.
    """

    # Subtract 2 from the stack to get the actual level. The parse tree root is always
    # on the stack, and the root node(s) in the document cannot have any indentation
    return max(len(self.stack) - 2, 0)

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
          indent = i / self.ws_per_indent
          floored = math.floor(indent)

          # Indentation must be an even multiple of previous indentation
          if floored < indent:
            raise ParseError("Uneven indentation level (expected multiple of %d)" % self.ws_per_indent)

          return floored

      # The line starts with whitespace but does not match with what we expect
      # the whitespace to be
      elif self.ws_char and c != self.ws_char:
        raise ParseError("Mismatched whitespace at start of line (use spaces or tabs, not both)")

      last = c

    return 0