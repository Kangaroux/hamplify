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

class RootNode(Node):
  def set_parent(self, parent):
    raise Exception("Called set_parent on root node")

class Text(Element):
  """ Plaintext element with no children
  """

  def __init__(self, text=""):
    self.text = text

  def render(self):
    return self.text

class Comment(Node):
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

class BaseBlock(object):
  def __init__(self, name=None, args=None):
    self.name = name
    self.args = args

class Block(BaseBlock, Node):
  """ A block that can span multiple lines.

  {% for x in list %}
    ...
  {% endfor %}
  """

  pass

class InlineBlock(BaseBlock, Element):
  """ A block that doesn't contain anything and only exists on a single line

  ...
  {% include "template.html" %}
  ...
  """

  pass

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

      if v is None:
        text += " %s" % k
      elif type(v) is int:
        text += " %s=%d" % (k, v)
      else:
        text += " %s=\"%s\"" % (k, v)

    text += self.END_OF_TAG

    return text

  def _get_class_string(self):
    """ Combines classes with the .class notation with the classes in the attribute
    dictionary, and returns it as a string
    """

    classes = self.attrs.get("class", "")

    if classes and self.classes:
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