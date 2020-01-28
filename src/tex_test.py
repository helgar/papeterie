#!/usr/bin/python3

""" Module to test texification. """

import unittest

from testing import PapeterieTestCase
from tex import texify


class TestTexifyText(PapeterieTestCase):
  """ Test texify. """

  def test_one_umlaut(self):
    """ Tests a string with exactly one umlaut. """
    string = "Erklärung"
    result = texify(string)
    self.assertEqual(result, u"Erkl\\\"arung")

  def test_multiple_umlauts(self):
    """ Tests a string with several umlauts. """
    string = u"Erklärbär"
    result = texify(string)
    self.assertEqual(result, u"Erkl\\\"arb\\\"ar")

  def test_one_big_s(self):
    """ Tests conversion of ss to sharp s. """
    string = "Straße"
    result = texify(string)
    self.assertEqual(result, u"Stra{\\\\ss}e")

  def test_no_umlaut(self):
    """ Tests no-op conversion if there aren't any umlauts. """
    string = "FooBar"
    result = texify(string)
    self.assertEqual(result, u"FooBar")

  def test_fix_empty_lines(self):
    """ Tests that fixing empty lines works. """
    string = "A\n\nB"
    result = texify(string)
    self.assertEqual(result, u"A\\\\\\\\\n\\\\leavevmode\\\\\\\\\nB")


if __name__ == '__main__':
  unittest.main()
