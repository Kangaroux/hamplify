TOKEN_TAG = "%"
TOKEN_CLASS = "."
TOKEN_ID = "#"
TOKEN_ATTR_WRAPPER = ("(", ")")
TOKEN_ATTR_SETVAL = "="
TOKEN_BLOCK = "-"
TOKEN_HTML_COMMENT = "-#"
TOKEN_COMMENT = "/"

BLOCKS = (TOKEN_BLOCK, TOKEN_COMMENT)
INDENTATION = (" ", "\t")

class ParseError(Exception):
  pass