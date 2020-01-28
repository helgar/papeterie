#!/usr/bin/python3

""" Unit tests for papeterie. """

import os
import shutil
import tempfile
import unittest

from testing import PapeterieTestCase

from pdflatex import PdfLatex
from output import BaseOutputController
from simple_template import SimpleTemplate
from snippets import Snippets
from papeterie import create_single_papeterie

class TestPapeterie(PapeterieTestCase):
  """ Tests the papeterie module. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_papeterie(self):
    """ Tests creating a single piece of papeterie. """
    result_path = os.path.join(self.test_dir, "result.pdf")

    pdflatex = PdfLatex()
    output = BaseOutputController(result_path)
    template_path = os.path.join(self.TESTDATA_FOLDER, "template.tex")
    template = SimpleTemplate(template_path)
    snippets = Snippets({"TEXT": "42"})

    create_single_papeterie(pdflatex, output, template, snippets)

    self.assertTrue(os.path.exists(output.pdf_path))


if __name__ == '__main__':
  unittest.main()
