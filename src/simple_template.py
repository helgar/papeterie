#/bin/python3

""" A really simple template engine. """

import re
import os
from copy import deepcopy


class TemplateException(Exception):
  """ Exception for this module. """


class SimpleTemplate:
  """ Very simple template.

  This provides a very simple templating engine, that replaces ALL CAPS
  placeholders with the given data. This is used to template latex files.
  We chose this simple version over existing templating engines like
  jinja and python's own mechanisms, because tex syntax and those engine's
  syntax was overlapping too much to not cause any headaces.

  filepath: string
    path of the template file

  """

  def __init__(self, filepath):
    if not filepath:
      raise TemplateException("No valid filename given.")

    if not os.path.exists(filepath):
      raise TemplateException("Template file %s does not exist." % filepath)

    with open(filepath, 'r', encoding='utf-8') as infile:
      self.__template = u"".join(infile.readlines())

  def __str__(self):
    return str(self.__template)

  def render(self, snippets):
    """ Substitutes placeholders with the content from the given snippets.

    snippets:
      a Snippets instance

    returns:
      a string containing the result of the substitution

    """
    result = deepcopy(self.__template)
    for (name, snippet) in snippets.to_dict().items():
      result = re.sub(name, snippet, result)
    return result
