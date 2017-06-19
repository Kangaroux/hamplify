import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

class FilterParser(BaseParser):
  def __init__(self, options=None):
    super(FilterParser, self).__init__(options)

  def parse(self, text):
    if text == FILTER_PLAIN:
      return FilterPlain()
    elif text == FILTER_JAVASCRIPT:
      return FilterJavascript()
    elif text == FILTER_CSS:
      return FilterCSS()

    return Text(text)