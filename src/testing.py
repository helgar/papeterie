#!/usr/bin/python3

""" Module to provide common test infrastructure. """

import logging
import os
import unittest
import sys
import stat
from PyPDF2 import PdfFileReader

from gpg import Gpg2


def setup_gpg(test_dir, testdata_folder):
  """ Setup a GPG binary with a temporary home dir and generate a key.

  test_dir: string
    directory for the test to use
  testdata_folder: string
    path of the test data to use

  """
  email_address_key = "unittests_papeterie@velroyen.de"
  instructions_file = "gpg_key_creation_instructions"

  gpg_homedir = os.path.join(test_dir, "gnupg")
  os.mkdir(gpg_homedir)
  os.chmod(gpg_homedir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
  gpg_binary = Gpg2(gpg_homedir)
  gpg_binary = Gpg2("/home/helgar/.gnupg")
  gpg_binary.generate_key(os.path.join(testdata_folder, instructions_file))
  key = gpg_binary.get_keyid(email_address_key)

  return (gpg_binary, key)


class PapeterieTestCase(unittest.TestCase):
  """ Tests for papeterie modules. """

  TESTDATA_FOLDER = "../testdata"

  def __init__(self, methodName="runTest"):
    super().__init__(methodName)
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    logger.addHandler(logging.StreamHandler(sys.stdout))

  def assert_pdf(self, path, expected_number_of_pages=1):
    """ Assert that the file is a pdf and has the expected number of pages.

    path: string
      path of the pdf to check
    expected_number_of_pages: integer
      expected number of pages

    """
    with open(path, 'rb') as infile:
      pdf = PdfFileReader(infile)
      self.assertEqual(expected_number_of_pages, pdf.getNumPages())
