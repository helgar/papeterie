#/bin/python3

""" Module to texify strings. """

import re


# TODO: add moar data from
# https://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&names=-&utf8=string-literal
UMLAUTS = {
    u'ü': u"\\\"u",
    u'ö': u"\\\"o",
    u'ä': u"\\\"a",
    u'Ü': u"\\\"U",
    u'Ö': u"\\\"O",
    u'Ä': u"\\\"A",
    u'é': u"\\\'e",
    u'ß': u"{\\\\\\\\ss}",
}

OTHER = {
    u'trasse': u"tra{\\\\\\\\ss}e",
    u'\n': u'\\\\\\\\\\\\\\\\\n',
}


def tex_strip(string):
  """ Strips the last added newline.

  This avoids a lot of headaches.

  string: string
    texified string

  returns: string
    texified string without the last replaced newline

  """
  if string[-5:] == u'\\\\\\\\\n':
    return string[:-5]
  return string


def fix_empty_lines(string):
  """ Special treatment for empty lines.

  Empty lines are converted to '\\\\' by default.
  However that confuses latex and hence, we replace those with
  '\\leavevmode\\\\'. More info: https://texfaq.org/FAQ-noline

  string: string
    string to fix

  returns: string
    fixed string

  """
  newline_only = u'\\\\\\\\'
  fixed_lines = []
  for line in string.split('\n'):
    if line == newline_only:
      line = u"\\\\leavevmode" + line
    fixed_lines.append(line)
  return '\n'.join(fixed_lines)


def texify(string):
  """ Convert a string to its representation in tex.

  string: string
    text to convert to tex

  returns:
    string in tex syntax

  """
  substitutions = OTHER
  substitutions.update(UMLAUTS)

  #logging.debug("String before texify: %s", string)
  for (key, value) in substitutions.items():
    string = re.sub(key, value, string)
  #logging.debug("String after texify: %s", string)
  string = fix_empty_lines(string)
  return tex_strip(string)
