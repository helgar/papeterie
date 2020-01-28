#!/usr/bin/python3

""" Unit tests for serial. """

import logging
import os
import shutil
import tempfile
import unittest
from argparse import Namespace

from testing import PapeterieTestCase

from letter import run


def setup_args(input_dir, snippets, output_path, keep_tmp=True, defaults=None):
  """ Assembles a Namespace instance just as if the user had specified args.

  See letter.py for description of the arguments.

  returns: Namespace
    the namespace instance with the arguments set

  """
  args = Namespace()
  args.__setattr__("input_dir", input_dir)
  args.__setattr__("snippets", snippets)
  args.__setattr__("output_file", output_path)
  args.__setattr__("keep_tmp", keep_tmp)
  args.__setattr__("defaults", defaults)
  return args


class TestLetter(PapeterieTestCase):
  """ Tests the letter module. """

  DATA_FOLDER = "../data/"

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_letter_en(self):
    """ Tests rendering an informal letter, American style. """
    snippets_file = os.path.join(self.DATA_FOLDER, "example_snippets_letter.pap")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "letter_en")
    args = setup_args(input_dir, snippets_file, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path)

  def test_letter_de(self):
    """ Tests rendering an informal letter, German style. """
    snippets_file = os.path.join(self.DATA_FOLDER, "example_snippets_letter.pap")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "letter_de")
    args = setup_args(input_dir, snippets_file, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path)

  def test_letter_formal_en(self):
    """ Tests rendering an formal letter, American style. """
    snippets_file = os.path.join(self.DATA_FOLDER, "example_snippets_letter_formal.pap")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "letter_formal_en")
    args = setup_args(input_dir, snippets_file, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path)

  def test_letter_formal_de(self):
    """ Tests rendering an formal letter, German style. """
    snippets_file = os.path.join(self.DATA_FOLDER, "example_snippets_letter_formal.pap")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "letter_en")
    args = setup_args(input_dir, snippets_file, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path)


if __name__ == '__main__':
  unittest.main()
