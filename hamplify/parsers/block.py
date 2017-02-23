import re

from .config import *
from hamplify.element import *

regex_block = re.compile(r'- *(\w+)(.*)')

class BlockParser:
  """ Blocks are used in template engines like Django Jinja2 for providing 
  some realtime processing of context data
  """

  def parse(self, text):
    # Handle comment blocks
    if text.startswith(TOKEN_HTML_COMMENT):
      return Comment().add_child(Text(text[len(TOKEN_HTML_COMMENT):]))
    elif text.startswith(TOKEN_COMMENT):
      return Comment(render=False).add_child(Text(text[len(TOKEN_COMMENT):]))

    match = regex_block.match(text)

    if not match:
      raise ParseError("Encountered a block with no arguments")

    return Block(match.group(1), match.group(2).strip())