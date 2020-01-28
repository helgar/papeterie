#!/usr/bin/python3

""" Module to test the configuration module. """

import unittest

from testing import PapeterieTestCase
import configuration


class TestLoadFromJson(PapeterieTestCase):
  """ Tests for loading config files from JSON. """

  def test_happy_config(self):
    """ Valid config. """
    config = configuration.config_from_json("../testdata/")
    self.assertTrue(config)


if __name__ == '__main__':
  unittest.main()
