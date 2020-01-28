#!/usr/bin/python3

""" Unit tests for serial papeterie that require human interaction.

These tests cannot be invoked automatically, because they need a human to type in
the password of the GPG key. This is by design as this simulates the real set up
best.

"""

import logging
import os
import re
import shutil
import tempfile
import unittest
from argparse import Namespace
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from testing import PapeterieTestCase, setup_gpg

from serial import run

# pylint: disable=too-many-arguments
# Yeah, we could that that in a builder-like pattern.

def setup_args(recipient_file, input_dir, output_path, gpg_key=None, gpg_homedir=None,
               keep_tmp=True):
  """ Sets up a Namespace instance just as if the user had specified commandline arguments.

  See serial.py for details on the arguments.

  returns Namespace
    a Namespace instance containing the specified arguments

  """
  args = Namespace()
  args.__setattr__("recipient_file", recipient_file)
  args.__setattr__("input_dir", input_dir)
  args.__setattr__("gpg_key", gpg_key)
  args.__setattr__("gpg_homedir", gpg_homedir)
  args.__setattr__("output_file", output_path)
  args.__setattr__("keep_tmp", keep_tmp)
  return args

# pylint: disable=too-many-arguments


def extract_text_from_pdf(file_path, page_idx):
  """ Extract the plain text from a PDF page.

  file_path: string
    path of the PDF file
  page_idx: integer
    index of page to extract

  returns: string

  """
  resource_manager = PDFResourceManager()
  stream = StringIO()
  device = TextConverter(resource_manager, stream, codec='utf-8', laparams=LAParams())
  interpreter = PDFPageInterpreter(resource_manager, device)
  with open(file_path, 'rb') as infile:
    pages = list(PDFPage.get_pages(infile, set(), maxpages=0, password="",
                                   caching=True, check_extractable=True))
    interpreter.process_page(pages[page_idx])
  device.close()
  page_txt = stream.getvalue()
  stream.close()
  return page_txt


def extract_signed_message_from_text(intext):
  """ Extract a signed message from a text.

  intext: string
    text containing one signed message

  returns: string
    the signed message and nothing else

  """
  begin = "-----BEGIN PGP SIGNED MESSAGE-----"
  end = "-----END PGP SIGNATURE-----"
  pattern = "%s(.+?)%s" % (begin, end)

  match = re.search(pattern, intext, re.DOTALL)
  if match:
    return "%s%s%s" % (begin, match.group(1), end)
  return None


class TestSerial(PapeterieTestCase):
  """ Tests the serial module. """

  DATA_FOLDER = "../data/"

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()
    (self.gpg, self.key) = setup_gpg(self.test_dir, self.TESTDATA_FOLDER)

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_savethedate_card_signed(self):
    """ Tests creating signed cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_savethedate_card_signed")
    args = setup_args(recipient_file, input_dir, output_path, gpg_key=self.key,
                      gpg_homedir=self.gpg.homedir)

    run(args, lambda x: None)

    self.assert_pdf(output_path, 12)

  def test_example_signature(self):
    """ Tests creating a document with a signature. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_signature")
    args = setup_args(recipient_file, input_dir, output_path, gpg_key=self.key,
                      gpg_homedir=self.gpg.homedir)

    run(args, lambda x: None)

    expected_number_of_pages = 6
    self.assert_pdf(output_path, expected_number_of_pages)

    # TODO: currently only the 2nd and 5th signed message can be verified.
    # Fix by finding out how to extract umlauts from PDFs properly.
    for idx in [2, 5]: # $range(expected_number_of_pages):
      page_txt = extract_text_from_pdf(output_path, idx)
      signed_message = extract_signed_message_from_text(page_txt)

      outfile_path = os.path.join(self.test_dir, "text_%s.asc" % idx)
      with open(outfile_path, 'w') as outfile:
        outfile.write(signed_message)

      self.gpg.check_signature(outfile_path)


if __name__ == '__main__':
  unittest.main()
