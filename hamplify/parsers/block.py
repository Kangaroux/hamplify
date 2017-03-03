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

  def parse(self, text, sibling=None):
    if not self.options.get("engine"):
      raise ParseError("Block support has not been set")

    match = regex_block.match(text)

    if not match:
      raise ParseError("Encountered a block with no arguments")

    name = match.group(1)
    args = match.group(2)

    if self.options.get("engine") == ENGINE_DJANGO:
      return self.new_block(DJANGO_BLOCKS, name, args, sibling)
    elif self.options.get("engine") == ENGINE_JINJA:
      return self.new_block(JINJA_BLOCKS, name, args, sibling)
    else:
      return self.new_inline_block(name, args)

  def new_block(self, block_list, name, args, sibling):
    """ Returns a new Block element if the block is not inline for the given
    template engine. Otherwise returns an inline block
    """

    # Two blocks next to each other need to be linked
    if sibling and type(sibling) is Block and len(sibling.tags) > 2:
      for k in block_list:
        if name in sibling.tags[2:]:
          block = Block()

          block.name = name
          block.args = args[1:]
          block.tags = sibling.tags
          block.linked_to = sibling

          sibling.render_end_tag = False

          return block

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