#!/usr/bin/python3

""" Unit tests for texfile. """

import os
import shutil
import tempfile
import unittest

from testing import PapeterieTestCase
from pdflatex import PdfLatex, PdfLatexException


class TestPdfLatex(PapeterieTestCase):
  """ Tests the pdf module. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_pdflatex(self):
    """ Test running pdflatex. """
    texfile_orig = os.path.join(self.TESTDATA_FOLDER, "template_card_result.tex")
    texfile = os.path.join(self.test_dir, "tex.tex")
    shutil.copy(texfile_orig, texfile)
    self.assertTrue(os.path.exists(texfile))

    pdflatex = PdfLatex()
    pdflatex.run(self.test_dir, "tex", texfile)

    pdf = os.path.join(self.test_dir, "tex.pdf")
    self.assertTrue(os.path.exists(pdf))

  def test_pdflatex_input_missing(self):
    """ Test running pdflatex when the input file is missing. """
    texfile = os.path.join(self.test_dir, "idontexist.tex")

    pdflatex = PdfLatex()
    with self.assertRaises(PdfLatexException):
      pdflatex.run(self.test_dir, "tex", texfile)


if __name__ == '__main__':
  unittest.main()
