#!/usr/bin/python3

""" Unit test for the recipient module. """

import unittest

from testing import PapeterieTestCase
from recipient import Recipient, RecipientException


class TestRecipient(PapeterieTestCase):
  """ Tests for the Recipient class. """

  def test_valid_recipient(self):
    """ Test with valid recipient data. """
    headerline = ["Opening", "Closing", "Theme"]
    dataline = ["Dear brother,", "Yours truly, Lisa and Millhouse", "Cthulhu"]

    result = Recipient(headerline, dataline)

    # pylint: disable=no-member
    self.assertEqual("Dear brother,", result.Opening)
    # pylint: enable=no-member
    self.assertEqual("Cthulhu", result.to_dict()["Theme"])

  def test_missing_data(self):
    """ Test with missing data value. """
    headerline = ["Opening", "Theme"]
    dataline = ["Dear brother,"]

    with self.assertRaises(RecipientException):
      Recipient(headerline, dataline)

  def test_superfluous_data(self):
    """ Test with superfluous data value. """
    headerline = ["Opening"]
    dataline = ["Dear brother,", "Cthulhu"]

    with self.assertRaises(RecipientException):
      Recipient(headerline, dataline)

  def test_empty_header(self):
    """ Test with an empty header. """
    headerline = []
    dataline = []

    with self.assertRaises(RecipientException):
      Recipient(headerline, dataline)


if __name__ == '__main__':
  unittest.main()
