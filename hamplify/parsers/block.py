import re

from hamplify.config import *
from hamplify.element import *

regex_block = re.compile(r'- *(\w+)(.*)')

class BlockParser:
  """ Blocks are used in template engines like Django Jinja2 for providing 
  some realtime processing of context data
  """

  def parse(self, text):
    match = regex_block.match(text)

    if not match:
      raise ParseError("Encountered a block with no arguments")

    return Block(match.group(1), match.group(2).strip())