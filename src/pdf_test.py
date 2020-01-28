#!/usr/bin/python3

""" Unit tests for pdf. """

import os
import shutil
import tempfile
import unittest

from testing import PapeterieTestCase
from pdf import merge_pdfs


class TestMergePdfs(PapeterieTestCase):
  """ Tests merging PDF files. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_merge_pdfs(self):
    """ Test merging pdfs. """
    pattern = "%s/card*.pdf" % self.TESTDATA_FOLDER
    result = os.path.join(self.test_dir, "result.pdf")

    merge_pdfs(pattern, result)

    self.assert_pdf(result, 2)


if __name__ == '__main__':
  unittest.main()
