class Element:
  parent = None

  def render():
    pass

class Node(Element):
  children = []

  def add_child(self, e):
    self.children.append(e)
    e.parent = self

class Text(Element):
  def __init__(self, text=""):
    self.text = text

class Tag(Node):
  def __init__(self, tag="div", classes=None, dom_id="", attrs=None):
    self.tag = tag

    if classes == None:
      self.classes = []
    else:
      self.classes = classes

    self.id = dom_id

    if attrs == None:
      self.attrs = {}
    else:
      self.attrs = attrs

  def __repr__(self):
    return "<%s class='%s' id='%s'>" % (self.tag, ",".join(self.classes), self.id)