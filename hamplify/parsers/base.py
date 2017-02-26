class BaseParser(object):
  def __init__(self, options=None):
    if options is None:
      options = {}

    self.options = options

  def parse(self, text):
    pass