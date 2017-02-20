TOKEN_TAG = "%"
TOKEN_CLASS = "."
TOKEN_ID = "#"
TOKEN_ATTR_WRAPPER = ("(", ")")
TOKEN_ATTR_SETVAL = "="

WHITESPACE = (" ", "\t")

class ParseError(Exception):
  pass