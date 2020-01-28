#!/usr/bin/python3

""" Unittest for the csv2recipients module. """

import os
import unittest

from testing import PapeterieTestCase
import csv2recipients


class TestCsv2Recipients(PapeterieTestCase):
  """ Tests for load_recipients. """

  FILE_VALID = "recipients_valid.csv"
  FILE_ONLY_HEADER = "recipients_onlyheader.csv"
  FILE_EMPTY = "recipients_empty.csv"

  def test_happy_file(self):
    """ Test with a file that has valid content. """
    testfile = os.path.join(self.TESTDATA_FOLDER, self.FILE_VALID)
    recipients = csv2recipients.load_recipients(testfile)
    self.assertEqual(2, len(recipients))

  def test_only_header(self):
    """ Test with a file which has a header only. """
    testfile = os.path.join(self.TESTDATA_FOLDER, self.FILE_ONLY_HEADER)
    with self.assertRaises(csv2recipients.Csv2RecipientsException):
      csv2recipients.load_recipients(testfile)

  def test_empty_file(self):
    """ Test with an empty file (not even a header). """
    testfile = os.path.join(self.TESTDATA_FOLDER, self.FILE_EMPTY)
    with self.assertRaises(csv2recipients.Csv2RecipientsException):
      csv2recipients.load_recipients(testfile)


if __name__ == '__main__':
  unittest.main()
