import unittest

from hamplify.element import *
from hamplify.config import *
from hamplify.parsers.parser import Parser

class TestFullParser(unittest.TestCase):
  p = None

  def setUp(self):
    self.p = Parser()

  def test_cant_pop_empty_stack(self):
    self.p._reset()

    with self.assertRaises(Exception):
      self.p._pop()

  def test_single_line_indentation(self):
    self.p._reset()
    assert None == self.p._get_indentation("")

    self.p._reset()
    assert None == self.p._get_indentation("  ")

    self.p._reset()
    assert 0 == self.p._get_indentation("text")

    self.p._reset()
    assert 1 == self.p._get_indentation("  text")
    assert self.p.ws_per_indent == 2
    assert self.p.ws_char == " "

  def test_indentation(self):
    self.p._reset()
    assert 0 == self.p._get_indentation("some text  ")
    assert 1 == self.p._get_indentation("  Indented")
    assert 2 == self.p._get_indentation("    Some more")
    assert None == self.p._get_indentation("        ")
    assert 1 == self.p._get_indentation("  Back down")

    assert 0 == self.p._get_indentation("- for x in list")
    assert 1 == self.p._get_indentation("  {{x}}")

  def test_mixed_indentation(self):
    self.p._reset()
    self.p.ws_per_indent = 2
    self.p.ws_char = " "

    with self.assertRaises(ParseError):
      self.p._get_indentation("\tTabs")

    with self.assertRaises(ParseError):
      self.p._get_indentation("\t  Mixed")

    with self.assertRaises(ParseError):
      self.p._get_indentation("  \tMixed")

  def test_uneven_indentation(self):
    self.p._reset()
    self.p.ws_per_indent = 4
    self.p.ws_char = " "

    with self.assertRaises(ParseError):
      self.p._get_indentation("  2 spaces instead of 4")

  def test_indentation_jump(self):
    with self.assertRaises(ParseError):
      self.p.parse("""
!!!
%html
  %head
      %title too much indentation
        """)

  def test_multiline(self):
    html = self.p.parse("""
!!!
%html
  %head
    %title My cool title
  %body
    .container
      %p some text
      / comment you can't see %tag.blah
        still a comment
         %  bad tag

      -# HTML comment
         some stuff
  """)

    assert (html.render() == "<!DOCTYPE html><html><head><title>My cool title</title></head><body>"
      "<div class=\"container\"><p>some text</p><!-- HTML comment\n some stuff --></div></body></html>")

  def test_blocks(self):
    self.p = Parser({
      "engine": ENGINE_DJANGO
    })

    html = self.p.parse("""
- for x in list
  {{x}}
- if condition
  - if another condition
    something
    - custom_tag
  %a(href="#") link
- else
  {{stuff}}
some text
%p blah
      """)

    assert (html.render() == '{% for x in list %}{{x}}{% endfor %}{% if condition %}'
      '{% if another condition %}something{% custom_tag %}{% endif %}'
      '<a href="#">link</a>{% else %}{{stuff}}{% endif %}some text<p>blah</p>')

  # Verifies that the parse error is generating the correct response
  def test_parse_error(self):
    try:
      self.p.parse("""
  %tag
        """)
    except ParseError as pe:
      s = str(pe)
      assert "line 2" in s
      assert "indentation" in s
      assert "%tag" in s

  def test_plain_filter(self):
    html = self.p.parse("""
%p a paragraph
:plain
  some text
  .asdf
   %p blah
%a link
      """)

    assert html.render() == '<p>a paragraph</p>some text\n.asdf\n %p blah<a>link</a>'

  def test_javascript_filter(self):
    html = self.p.parse("""
%p a paragraph
:javascript
  var myVar = "asdf";
  // Comment
%a link
      """)

    assert html.render() == '<p>a paragraph</p><script type="text/javascript">var myVar = "asdf";\n// Comment</script><a>link</a>'

  def test_css_filter(self):
    html = self.p.parse("""
%p a paragraph
:css
  .class {
    color: #333;
  }

  /* Comment */
  #some-id {
    margin: 0px;
  }
%a link
      """)

    assert (html.render() == '<p>a paragraph</p><style type="text/css">.class {\n  color: #333;\n}'
      '\n\n/* Comment */\n#some-id {\n  margin: 0px;\n}</style><a>link</a>')

  def test_conditional_comment(self):
    html = self.p.parse("""
-#[if IE]  
  %script(src="run_this.js")

  :plain
    %test
      """)

    assert html.render() == '<!--[if IE]><script src="run_this.js"></script>%test<![endif]-->'