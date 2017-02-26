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
JINJA_BLOCKS = (
  ("block", "endblock"),
  ("call", "endcall"),
  ("for", "endfor", "else"),
  ("filter", "endfilter"),
  ("if", "endif", "elif", "else"),
  ("macro", "endmacro"),
  ("set", "endset"),
)

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

class ParseError(Exception):
  pass