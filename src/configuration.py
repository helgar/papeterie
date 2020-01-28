#/bin/python3

""" Module to load a configuration from a JSON file. """

import json
import os

CONFIG_FILE = "config.json"
SNIPPETS = "snippets"
SIGNED_SNIPPETS = "signed_snippets"
SNIPPET = "snippet"
KEY = "key"


def config_from_json(input_dir):
  """ Loads the JSON file and returns a Configuration object. """
  config_file = os.path.join(input_dir, CONFIG_FILE)
  with open(config_file, 'r') as config_fp:
    config = json.load(config_fp)
  return Configuration(
      input_dir,
      config.get(SNIPPETS, None),
      config.get(SIGNED_SNIPPETS, None))


class Configuration():
  """ Manages the configuration of the papeterie. """

  def __init__(self, input_dir, snippets=None, signed_snippets=None):
    self.__input_dir = input_dir
    self.__snippets = {k: os.path.join(input_dir, v)
                       for (k, v) in snippets.items()} if snippets else {}
    self.__signed_snippets = signed_snippets if signed_snippets else {}

  @property
  def snippets(self):
    """ The dictionary of snippet names to snippet template files. """
    return self.__snippets

  @property
  def tex_template(self):
    """ The tex template file for this papeterie. """
    return os.path.join(self.__input_dir, "papeterie.tex")

  @property
  def signed_snippets(self):
    """ The mapping of signed snippets to original snippets. """
    return self.__signed_snippets
