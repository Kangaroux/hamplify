import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

regex_block = re.compile(r'- *(\w+)(.*)')

class BlockParser(BaseParser):
  """ Blocks are used in template engines like Django and Jinja2 for providing 
  some realtime processing of context data
  """

  def __init__(self, options=None):
    super(BlockParser, self).__init__(options)

  def parse(self, text):
    if not self.options.get("engine"):
      raise ParseError("Block support has not been set")

    match = regex_block.match(text)

    if not match:
      raise ParseError("Encountered a block with no arguments")

    if self.options.get("engine") == ENGINE_DJANGO:
      return self.new_block(DJANGO_BLOCKS, match.group(1), match.group(2))
    elif self.options.get("engine") == ENGINE_JINJA:
      return self.new_block(JINJA_BLOCKS, match.group(1), match.group(2))

  def new_block(self, block_list, name, args):
    """ Returns a new Block element if the block is not inline for the given
    template engine. Otherwise returns an inline block
    """

    for k in block_list:
      if name == k[0]:
        block = Block()

        block.name = name
        block.args = args[1:]
        block.tags = k

        return block

    return self.new_inline_block(name, args)

  def new_inline_block(self, name, args):
    block = InlineBlock()

    block.name = name
    block.args = args[1:]

    return block