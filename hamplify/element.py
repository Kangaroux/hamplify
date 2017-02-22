class Element:
  """ Base element
  """

  parent = None

  def render():
    pass

class Node(Element):
  """ An element that can have children
  """

  def __init__(self):
    self.children = []

  def add_child(self, e):
    self.children.append(e)
    e.parent = self

    return self

class Text(Element):
  """ Plaintext element with no children
  """

  def __init__(self, text=""):
    self.text = text

class Comment(Node):
  """ Comment block
  """

  def __init__(self, render_comment=True):
    super().__init__()

    # Whether this comment should be rendered or not. Comments that are rendered
    # appear as an html comment <!-- --> 
    self.render_comment = render_comment

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

  def __init__(self, tag="div", classes=None, dom_id="", attrs=None):
    super().__init__()

    self.attrs = attrs or {}
    self.classes = classes or []
    self.id = dom_id
    self.tag = tag