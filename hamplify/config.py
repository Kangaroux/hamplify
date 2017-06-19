TOKEN_ATTR_SETVAL = "="
TOKEN_ATTR_WRAPPER = ("(", ")")
TOKEN_BLOCK = "-"
TOKEN_CLASS = "."
TOKEN_COMMENT = "/"
TOKEN_DOCTYPE = "!!!"
TOKEN_FILTER = ":"
TOKEN_HTML_COMMENT = "-#"
TOKEN_ID = "#"
TOKEN_TAG = "%"

TAG_TOKENS = (TOKEN_TAG, TOKEN_CLASS, TOKEN_ID)
COMMENT_TOKENS = (TOKEN_HTML_COMMENT, TOKEN_COMMENT)
INDENTATION = (" ", "\t")

ENGINE_DJANGO = "django"
ENGINE_JINJA = "jinja"
ENGINES = ("django", "jinja")

FILTER_PLAIN = TOKEN_FILTER + "plain"
FILTER_JAVASCRIPT = TOKEN_FILTER + "javascript"
FILTER_CSS = TOKEN_FILTER + "css"

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

""" These are blocks specific to Jinja/Django. They are rendered as {% ... %}{% ... %}

The syntax for defining a block is:

(opening_name, closing_name, [intermediate_name_1, intermediate_name_2, ...])

A `block` tag only has an opening and a closing tag, so it's defined as ("block", "endblock"),
and it looks like this:

{% block %}
  ...
{% endblock %}

However, an `if` statement could have an `elif` or `else` before the tag is fully closed, so it's
defined as ("if", "endif", "elif", "else"). We won't enforce that the elifs and elses come in the
right order, that's the template engine's job.

{% if condition %}
  ...
{% elif condition %}
  ...
{% else %}
  ...
{% endif %}
"""

DJANGO_BLOCKS = (
  ("autoescape", "endautoescape"),
  ("block", "endblock"),
  ("comment", "endcomment"),
  ("for", "endfor", "empty"),
  ("filter", "endfilter"),
  ("if", "endif", "elif", "else"),
  ("ifchanged", "endifchanged"),
  ("ifequal", "endifequal"),
  ("spaceless", "endspaceless"),
  ("verbatim", "endverbatim"),
  ("with", "endwith"),
)

JINJA_BLOCKS = (
  ("block", "endblock"),
  ("call", "endcall"),
  ("for", "endfor", "else"),
  ("filter", "endfilter"),
  ("if", "endif", "elif", "else"),
  ("macro", "endmacro"),
  ("set", "endset"),
)

class ParseError(Exception):
  def __init__(self, message, line_number=None, col=None, line=None, file_path=None):
    self.col = col
    self.line = line
    self.line_number = line_number
    self.message = message
    self.file_path = file_path

  def __str__(self):
    text = "Syntax error "

    if self.line_number:
      text += "on line %d " % self.line_number

    if self.col:
      text += "at col %d " % self.col

    if self.file_path:
      text += "in file %s" % self.file_path

    text = text.strip()

    text += "\n\n%s" % self.line
    text += "\n\nReason: %s" % self.message

    return text