#/bin/python3

""" Module to manage a collection of snippets. """

from copy import deepcopy
import logging


# Special snippet name to contain the path for pictures
PAPETERIEPICPATH = "PAPETERIEPICPATH"


class SnippetsException(Exception):
  """ Exception for this module. """


def from_snippets_string(snippet_names, snippets_string, check_completeness=True):
  """ Takes an iterable of snippet names and a string containing the snippets and creates
       a snippet collection from it.

  snippet_names:
    an iterable of snippet names
  snippets_string:
    a string containing the snippets in the form:

  SNIPPET_NAME1
  snippet1
  SNIPPET_NAME2
  snippet2

  check_completeness: boolean
    whether or not to check if all snippets of the names list are in the snippets string

  returns:
    a Snippets instance

  """
  snippet_dict = {}

  current_snippet_name = None
  current_snippet = ""
  for line in snippets_string.split("\n"):
    if line.strip() in set(snippet_names):
      if current_snippet != "":
        snippet_dict[current_snippet_name] = current_snippet.strip()
        current_snippet = ""
        current_snippet_name = None
      current_snippet_name = line.strip()
      continue
    current_snippet += line.strip() + "\n"
  snippet_dict[current_snippet_name] = current_snippet.strip()
  return from_dict(snippet_names, snippet_dict, check_completeness)


def from_file(names, snippet_file_path, check_completeness=True):
  """ Read a snippet collection from file.

  names: list of str
    list of snippet names in ALL CAPS as they appear in the templates.
  snippet_file_path: string
    path of the snippet file
  check_completeness: boolean
    whether or not to check if all snippets of the names list are in the snippets string

  returns
    a Snippets instance

  """
  with open(snippet_file_path, 'r', encoding='utf-8') as infile:
    snippet_str = u"".join(infile.readlines())
  return from_snippets_string(names, snippet_str, check_completeness=check_completeness)


def from_dict(names, snippet_dict, check_completeness=True):
  """ Creates a snippet collection based on a list of snippet names and a
      dictionary.

  names:
    list of snippet names in ALL CAPS as they appear in the templates.
  snippet_dict:
    dictionary of snippet names to snippets. The keys must be a superset of
    names.
  check_completeness: boolean
    whether or not to check if all snippets of the names list are in the snippets string

  returns:
    a Snippets instance.

  """
  if not names:
    raise SnippetsException("No names given.")

  if not snippet_dict:
    raise SnippetsException("No snippets given.")

  superfluous_snippets = []
  for key in snippet_dict:
    if key.upper() not in names:
      superfluous_snippets.append(key)
  for key in superfluous_snippets:
    logging.info("Removing superfluous snippet %s", key)
    del snippet_dict[key]

  result = Snippets(snippet_dict)

  if check_completeness:
    result.check_completeness(names)

  return result


class Snippets():
  """ A collection of snippets.

  Main purpose is to fill simple templates. Therefore, the list of snippet names must
  match the ALL CAPS placeholders in the template. ALL CAPS is enforced on construction.

  snippet_dict:
    a dictionray of snippet names to snippets.

  """
  def __init__(self, snippet_dict):
    self.__snippets = {k.upper(): v for (k, v) in snippet_dict.items()}
    self.__check_overlap()

  def __len__(self):
    return len(self.__snippets)

  def to_dict(self):
    """ Returns the dictionary of snippet names to snippets. """
    return deepcopy(self.__snippets)

  def __str__(self):
    """ Returns the string representation of the collection.

    Note: the snippets are ordered alphabetically by snippet name.

    Format:
    SNIPPETNAME1
    snippet1
    SNIPPETNAME2
    snippet2
    ...

    """
    string = ""
    names_ordered = list(self.__snippets.keys())
    names_ordered.sort()
    for name in names_ordered:
      logging.debug("Adding snippet to string: %s", name)
      string += name + "\n" + self.__snippets[name] + "\n"
    return string

  def check_completeness(self, names):
    """ Checks if all given snippet names are in the snippet collection.

    names: list of str
      list of snippet names

    raises: SnippetsException
      if at least one snippet from the snippet name list is not in the dictionary

    """
    for name in names:
      if not name.upper() in self.__snippets:
        raise SnippetsException("Required snippet %s is not in snippet dictionary: %s" %
                                (name, self.__snippets.keys()))

  def __check_overlap(self):
    """ Checks that no snippet name is a substring of another snippet name.

    This is to make sure that we don't mess up our stupid simple template mechanism.

    """
    for name in self.__snippets:
      for other_name in self.__snippets:
        if name != other_name:
          if name in other_name or other_name in name:
            raise SnippetsException(
                "Snippet name %s and %s are substrings of each other." % (
                    name, other_name))

  def subset(self, subset):
    """ Create a snippet collection that is a subset of another one.

    subset: set of strings
      set of snippet names, must be a subset of the original snippet name set

    returns:
      a new Snippets instance containing only the requested subset of snippets

    """
    return Snippets({name: self.__snippets[name] for name in subset})

  def renamed(self, name_map):
    """ Create a snippet collection by renaming the snippets of another one.

    name_map: dict of string to string
      mapping of original snippet names to new snippet names

    returns:
      a new Snippets instance with the keys being renamed
    """
    return Snippets({name_map[name]: snippet for (name, snippet) in self.__snippets.items()})

  # pylint: disable=invalid-name
  def transform(self, fn=(lambda x: x)):
    """ Creates a new snippets instance based on the original one, optionally by
        applying function fn to all snippets.

    fn: function str -> str
      a function to convert the original snippets to new snippets
      if not specified, this is the identify function

    returns:
      a new Snippets instance with transformed valued

    """
    return Snippets({name: fn(snippet) for (name, snippet) in self.__snippets.items()})
  # pylint: enable=invalid-name

  def merge_with(self, mergee, check_overlapping=True):
    """ Create a snippet collection by mergin two other ones.

    Note: if check_overlapping is  The key sets must be disjunct.

    mergee: Snippets
      a snippet collection
    check_overlapping: boolean
      whether or not to check that the key sets are disjunct

    returns:
      a new Snippets instance based on the original snippets with the new ones added
      (updating original snippets)

    """
    if check_overlapping:
      if set(self.to_dict().keys()).intersection(set(mergee.to_dict().keys())):
        raise SnippetsException("Snippet keys are overlapping.")

    new_dict = deepcopy(self.to_dict())
    new_dict.update(mergee.to_dict())
    return Snippets(new_dict)

  def add(self, name, snippet):
    """ Creates a snippet collection from the original with an additional snippet in it.

    Note: this does not test whether the additional snippet name is already present.

    name: string
      name of the additional snippet
    snippet: string
      content of the additional snippet

    """
    new_dict = deepcopy(self.to_dict())
    new_dict[name.upper()] = snippet
    return Snippets(new_dict)
