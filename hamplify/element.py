class Element:
  """ Base element
  """

  depth = 0
  parent = None

  def set_parent(self, parent):
    self.parent = parent
    self.depth = parent.depth + 1

  def render(self):
    """ Renders the element as text
    """

    return ""

class Node(Element):
  """ An element that can have children
  """

  def __init__(self):
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
    super().__init__()

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
      return "-->"
    else:
      return ""

class BaseBlock:
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

class Tag(Node):
  """ An html tag with an id, classes, and attributes
  """

  def __init__(self, tag="div", classes=None, dom_id=None, attrs=None):
    super().__init__()

    self.attrs = attrs or {}
    self.classes = classes or []
    self.id = dom_id
    self.tag = tag

  def _pre_render(self):
    text = "<%s" % self.tag

    # Combine the shorthand classes with ones in the attributes
    classes = self.attrs.get("class", "")

    if classes:
      classes += " "

    classes += " ".join(self.classes)

    if classes:
      self.attrs["class"] = classes

    if self.id:
      text += " id=\"%s\"" % self.id

    # Add the attributes
    for k, v in self.attrs.items():
      if v is None:
        text += " %s" % k
      elif type(v) is int:
        text += " %s=%d" % (k, v)
      else:
        text += " %s=\"%s\"" % (k, v)

    text += ">"

    return text

  def _post_render(self):
    return "</%s>" % self.tag