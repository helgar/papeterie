#!/usr/bin/python3

""" Unit tests for the jinja2snippet module. """

import os
import shutil
import tempfile
import unittest

from testing import PapeterieTestCase
import jinja2snippet
from recipient import Recipient


class TestJinja2Snippet(PapeterieTestCase):
  """ Tests the jingja2snippet module. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_happy_file(self):
    """ Tests whether a sane file is correctly rendered. """
    recipient = Recipient(["AddressLine1", "AddressLine2", "AddressLine3"],
                          ["Marge Simpson", "123 Baker St", "Springfield, CA"])
    template_file = os.path.join(self.TESTDATA_FOLDER, "address_jinja.txt")

    jinja_template = jinja2snippet.JinjaTemplate(template_file)
    result_string = jinja_template.render(recipient)

    expected = "Marge Simpson\n123 Baker St\nSpringfield, CA\n\n"
    self.assertEqual(result_string, expected)


if __name__ == '__main__':
  unittest.main()
