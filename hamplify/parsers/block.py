import re

from .config import *
from hamplify.element import *

regex_block = re.compile(r'- *(\w)(.*)')

class BlockParser:
  def parse(self, text):
    # Handle comment blocks
    if text.startswith(TOKEN_HTML_COMMENT):
      return Comment().add_child(Text(text[len(TOKEN_HTML_COMMENT):]))
    elif text.startswith(TOKEN_COMMENT):
      return Comment(render_comment=False).add_child(Text(text[len(TOKEN_COMMENT):]))

    # match = regex_block.match(text)
    # print(match.groups())