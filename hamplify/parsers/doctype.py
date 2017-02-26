import re

from .base import BaseParser
from hamplify.config import *
from hamplify.element import Text

doctypes = (
  (re.compile(r'!!!(?: 5)?$'), '<!DOCTYPE html>'),
  (re.compile(r'!!! 1\.0$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'),
  (re.compile(r'!!! strict$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'),
  (re.compile(r'!!! frameset$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'),
  (re.compile(r'!!! 1\.1$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'),
  (re.compile(r'!!! basic$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">'),
  (re.compile(r'!!! mobile$'), '<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" "http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">'),
  (re.compile(r'!!! rdfa$'), '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">')
)

class DoctypeParser(BaseParser):
  def __init__(self, options=None):
    super(DoctypeParser, self).__init__(options)
    
  def parse(self, text):
    text = text.strip().lower()

    for regex, html in doctypes:
      match = regex.match(text)

      if match:
        return Text(html)

    raise ParseError("Unrecognized doctype: '%s'" % text)