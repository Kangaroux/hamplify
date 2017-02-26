import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

class CommentParser(BaseParser):
  """ Parses out HTML and HAML comments:

  -# HTML comment (rendered)
  / HAML comment (not rendered)
  """

  def __init__(self, options=None):
    super(CommentParser, self).__init__(options)

  def parse(self, text):
    if text.startswith(TOKEN_HTML_COMMENT):
      return Comment().add_child(Text(text[len(TOKEN_HTML_COMMENT):]))
    elif text.startswith(TOKEN_COMMENT):
      return Comment(render=False).add_child(Text(text[len(TOKEN_COMMENT):]))

    return Text(text)