from collections import OrderedDict

from hamplify.config import ParseError

class Element(object):
  """ Base element
  """

  depth = 0
  parent = None

  def __init__(self):
    super(Element, self).__init__()

  def set_parent(self, parent):
    self.parent = parent

    if type(parent) is RootNode:
      self.depth = 0
    else:
      self.depth = parent.depth + 1

  def render(self):
    """ Renders the element as text
    """

    return ""

class Node(Element):
  """ An element that can have children
  """

  def __init__(self):
    super(Node, self).__init__()

    self.children = []

    # Whether this element's children should be rendered
    self.render_children = True

  def add_child(self, e):
    self.children.append(e)
    e.set_parent(self)

    return self

  def render(self):
    """ Renders this element, followed by its children, followed by any post rendering.
    All rendering code should go in _pre_render and _post_render.
    """

    text = self._pre_render()

    if self.render_children:
      text += self._render_children()
    
    text += self._post_render()

    return text

  def _pre_render(self):
    """ Renders the element before its children are rendered
    """

    return ""

  def _post_render(self):
    """ Renders the element after its children are rendered
    """

    return ""

  def _render_children(self):
    """ Renders each child
    """

    text = ""

    for e in self.children:
      text += e.render()

    return text

  def _parse_children(self):
    """ Whether this element should have its children parsed
    """

    return True

class RootNode(Node):
  def __init__(self):
    super(RootNode, self).__init__()

  def set_parent(self, parent):
    raise Exception("Called set_parent on root node")

class Text(Element):
  """ Plaintext element with no children
  """

  def __init__(self, text=""):
    super(Text, self).__init__()

    self.text = text

  def render(self):
    return self.text

  def is_empty(self):
    return len(self.text.strip()) == 0

class Filter(Node):
  def _parse_children(self):
    return False

  def _render_children(self):
    text = ""

    for i in range(len(self.children)):
      text += self.children[i].render()

      if i != len(self.children) - 1:
        text += "\n"

    # Strip any trailing newlines
    return text.rstrip("\n")

class Comment(Filter):
  """ Comment block
  """

  def __init__(self, render=True):
    super(Comment, self).__init__()

    # Whether this comment should be rendered or not. Comments that are rendered
    # appear as an html comment <!-- --> 
    self.render_children = render

  def _pre_render(self):
    if self.render_children:
      return "<!--"
    else:
      return ""

  def _post_render(self):
    if self.render_children:
      return " -->"
    else:
      return ""

class FilterPlain(Filter):
  pass

class FilterJavascript(Filter):
  def _pre_render(self):
    return '<script type="text/javascript">'

  def _post_render(self):
    return '</script>'

class FilterCSS(Filter):
  def _pre_render(self):
    return '<style type="text/css">'

  def _post_render(self):
    return '</style>'

class BaseBlock(object):
  def __init__(self):
    super(BaseBlock, self).__init__()

    self.name = None
    self.args = None

class Block(BaseBlock, Node):
  """ A block that can span multiple lines.

  {% for x in list %}
    ...
  {% endfor %}
  """

  def __init__(self):
    super(Block, self).__init__()

    # Some blocks (like if's) can have elifs and elses before 
    # the block is completely closed.
    self.linked_to = None
    self.render_end_tag = True

    # The tuple containing the tags this block uses
    # e.g. ("block", "endblock")
    self.tags = None

  def _pre_render(self):
    text = "{%% %s" % self.name

    if self.args:
      text += " %s" % self.args

    return text + " %}"

  def _post_render(self):
    if self.render_end_tag:
      return "{%% %s %%}" % self.tags[1]
    else:
      return ""

class InlineBlock(BaseBlock, Element):
  """ A block that doesn't contain anything and only exists on a single line

  ...
  {% include "template.html" %}
  ...
  """

  def __init__(self):
    super(InlineBlock, self).__init__()

  def render(self):
    text = "{%% %s" % self.name

    if self.args:
      text += " %s" % self.args

    return text + " %}"

class BaseTag(object):
  """ An html tag with an id, classes, and attributes
  """

  # What to use for the end of the tag (not to be confused with the closing tag, </tag>)
  END_OF_TAG = ">"

  def __init__(self):
    super(BaseTag, self).__init__()
    
    self.attrs = OrderedDict()
    self.classes = []
    self.id = None
    self.tag = ""

  def _pre_render(self):
    text = "<%s" % self.tag

    if self.id:
      text += " id=\"%s\"" % self.id

    classes = self._get_class_string()

    if classes:
      text += " class=\"%s\"" % classes
    
    # Add the attributes
    for k, v in self.attrs.items():
      # Skip if the ID was already defined
      if k == "id" and self.id:
        raise ParseError("Tag has both an #id and an id='', not sure which to use")
      elif k == "class":
        # Classes are inserted manually, above
        continue

      text += " " + v.render()

    text += self.END_OF_TAG

    return text

  def _get_class_string(self):
    """ Combines classes with the .class notation with the classes in the attribute
    dictionary, and returns it as a string
    """

    classes = self.attrs.get("class", None)

    # No classes were set in the attributes
    if not classes:
      return " ".join(self.classes)

    classes = classes.value

    # Make room for the classes set in the tag
    if self.classes:
      classes += " "

    classes += " ".join(self.classes)

    return classes

class Tag(BaseTag, Node):
  """ A tag that can have children.

  <tag>...</tag>
  """

  def __init__(self):
    super(Tag, self).__init__()

  def _post_render(self):
    return "</%s>" % self.tag

class SelfClosingTag(BaseTag, Element):
  """ A self closing tag that has no children

  <tag />
  """

  def __init__(self):
    super(SelfClosingTag, self).__init__()

  END_OF_TAG = " />"

  def render(self):
    return self._pre_render()