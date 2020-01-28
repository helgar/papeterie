#/bin/python3

""" Module for the recipient class. """

import logging

class RecipientException(Exception):
  """ Exceptions of this module. """

class Recipient():
  """ Represents one recipient of the papeterie. """

  def __init__(self, headerline, recipient):
    if not headerline:
      raise RecipientException("No headerline given.")

    if len(headerline) != len(recipient):
      raise RecipientException("Data line does not match headerline.")

    self.__fields = headerline
    for (idx, headerfield) in enumerate(headerline):
      self.__setattr__(headerfield, recipient[idx])
      logging.debug(
          "Set attribute %s to %s.",
          headerfield, self.__getattribute__(headerfield))

  def __str__(self):
    string = ""
    for field in self.__fields:
      string += field + ": " + self.__getattribute__(field) + "\n"
    return string

  def to_dict(self):
    """ Return's the recipient's data as dictionary. """
    dictionary = {}
    for field in self.__fields:
      dictionary[field] = self.__getattribute__(field)
    return dictionary
