#/bin/python3

""" Unit tests for simple template. """

import shutil
import os
import tempfile
import unittest

from testing import PapeterieTestCase
from simple_template import SimpleTemplate
from snippets import Snippets


class TestSimpleTemplate(PapeterieTestCase):
  """ Tests the snippet_collector module. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_template(self):
    """ Tests rendering of a template. """
    template_file = os.path.join(self.TESTDATA_FOLDER, "template.tex")
    content = Snippets({"TEXT": "text"})

    template = SimpleTemplate(template_file)
    result = template.render(content)

    expected_file = os.path.join(self.TESTDATA_FOLDER, "template_result.tex")
    with open(expected_file, 'r', encoding='utf-8') as infile:
      expected = u"".join(infile.readlines())

    self.assertEqual(expected, result)


if __name__ == '__main__':
  unittest.main()
