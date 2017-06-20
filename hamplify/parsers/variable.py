import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import *

regex_variable = re.compile(r'^= *(.*)')

class VariableParser(BaseParser):
  """ Blocks are used in template engines like Django and Jinja2 for providing 
  some realtime processing of context data
  """

  def __init__(self, options=None):
    super(VariableParser, self).__init__(options)

  def parse(self, text):
    if not self.options.get("engine"):
      raise ParseError("Variable support has not been set")

    match = regex_variable.match(text)

    if not match or not match.group(1):
      raise ParseError("Encountered a blank variable")

    return Variable(match.group(1).strip())