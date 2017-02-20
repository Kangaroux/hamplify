import math

from .config import *
from hamplify.element import *

class Parser:
  def _reset(self):
    self.ws_per_indent = None
    self.ws_char = None
    self.root = Node()
    self.cursor = self.root
    self.stack = []

  def parse(self, text):
    text = text.split("\n")

    for line in text:
      indentation = self._get_indentation(line)
      line = line.lstrip()

  def _get_indentation(self, line):
    """ Calculates the indentation level of the line
    """

    last = None

    for i in range(len(line)):
      c = line[i]

      if c not in WHITESPACE:
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