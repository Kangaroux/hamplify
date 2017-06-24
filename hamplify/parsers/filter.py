import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

class FilterParser(BaseParser):
  def __init__(self, options=None):
    super(FilterParser, self).__init__(options)

  def parse(self, text):
    if self._matches(text, FILTER_PLAIN):
      return FilterPlain()
    elif self._matches(text, FILTER_JAVASCRIPT):
      return FilterJavascript()
    elif self._matches(text, FILTER_CSS):
      return FilterCSS()

    return Text(text)

  def _matches(self, text, filters):
    if not text.startswith(TOKEN_FILTER):
      return False

    text = text[len(TOKEN_FILTER):]

    if type(filters) is str:
      return text == filters
    elif type(filters) is list or type(filters) is tuple:
      return text in filters