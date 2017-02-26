TOKEN_TAG = "%"
TOKEN_CLASS = "."
TOKEN_ID = "#"
TOKEN_ATTR_WRAPPER = ("(", ")")
TOKEN_ATTR_SETVAL = "="
TOKEN_BLOCK = "-"
TOKEN_HTML_COMMENT = "-#"
TOKEN_COMMENT = "/"
TOKEN_DOCTYPE = "!!!"

TAG_TOKENS = (TOKEN_TAG, TOKEN_CLASS, TOKEN_ID)
COMMENT_TOKENS = (TOKEN_HTML_COMMENT, TOKEN_COMMENT)
INDENTATION = (" ", "\t")

# List of tags which are considered self closing
SELF_CLOSING_TAGS = (
  "area",
  "base",
  "br",
  "col",
  "command",
  "embed",
  "hr",
  "img",
  "input",
  "keygen",
  "link",
  "meta",
  "param",
  "source",
  "track",
  "wbr"
)

class ParseError(Exception):
  pass