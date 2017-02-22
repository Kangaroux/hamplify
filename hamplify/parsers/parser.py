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
      indentation = self._get_indentation(line)
      line = line.lstrip()

      level = self._indent_level()

      # Indentation can only increase at a rate of once per line
      if indentation > (level + 1):
        raise ParseError("Indentation jumped too much (previous level was %d,"
          " now at %d)" % (level, floored))
      else:
        # If the indentation didn't increase, then some elements 
        # from the stack need to be popped
        while indentation <= level:
          self._pop()
          level -= 1

      if not line:
        self._push(Text(line))
      elif line.startswith(TOKEN_TAG):
        self._push(self.tag_parser.parse(line))
      else:
        for b in BLOCKS:
          if line.startswith(b):
            self._push(self.block_parser.parse(line))
            break

  def _push(self, element):
    """ Pushes a node into the stack and updates the cursor
    """

    self.stack.append(element)
    self.cursor.add_child(element)
    self.cursor = element

  def _pop(self):
    """ Removes the element at the top of the stack and returns it
    """

    if len(self.stack) == 1:
      raise Exception("Tried to pop stack while it was empty")

    e = self._top()
    self.stack = self.stack[:-1]
    self.cursor = self._top()

    return e

  def _top(self):
    """ Gets the top element on the stack
    """

    return self.stack[-1]

  def _indent_level(self):
    """ Gets the current indentation level
    """

    return len(self.stack)

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