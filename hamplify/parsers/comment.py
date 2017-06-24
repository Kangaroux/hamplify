import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

# Conditional comment regex
regex_cc = re.compile(r'^\[(.*)\]')

class CommentParser(BaseParser):
  """ Parses out HTML and HAML comments:

  -# HTML comment (rendered)
  / HAML comment (not rendered)
  """

  def __init__(self, options=None):
    super(CommentParser, self).__init__(options)

  def parse(self, text):
    if text.startswith(TOKEN_HTML_COMMENT):
      text = text[len(TOKEN_HTML_COMMENT):]

      # Check if this is a conditonal comment
      match = regex_cc.match(text.rstrip())
      if match:
        return ConditionalComment(match.group(1))

      return Comment().add_child(Text(text))
    elif text.startswith(TOKEN_COMMENT):
      return Comment(render=False).add_child(Text(text[len(TOKEN_COMMENT):]))

    return Text(text)