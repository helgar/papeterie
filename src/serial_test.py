#!/usr/bin/python3

""" Unit tests for serial papeterie.

Note: This covers all examples that do not require GPG signing. Those are found
in serial_test_interactive.py.

"""

import logging
import os
import shutil
import tempfile
import unittest
from argparse import Namespace

from testing import PapeterieTestCase

from serial import run


def setup_args(recipient_file, input_dir, output_path,
               keep_tmp=True):
  """ Sets up a Namespace instance just as if the user had specified commandline arguments.

  See serial.py for details on the arguments.

  returns Namespace
    a Namespace instance containing the specified arguments

  """
  args = Namespace()
  args.__setattr__("recipient_file", recipient_file)
  args.__setattr__("input_dir", input_dir)
  args.__setattr__("gpg_key", None)
  args.__setattr__("gpg_homedir", None)
  args.__setattr__("output_file", output_path)
  args.__setattr__("keep_tmp", keep_tmp)
  return args


class TestSerial(PapeterieTestCase):
  """ Tests the serial module. """

  DATA_FOLDER = "../data/"

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_savethedate_card_signed(self):
    """ Tests creating signed save-the-date cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_savethedate_card")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_invitation_themed(self):
    """ Tests creating themed invitation cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_invitation_themed")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_invitation_multilingual(self):
    """ Tests creating themed invitation cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_invitation_multilingual")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_invitation_customtext(self):
    """ Tests creating themed invitation cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_invitation_customtext")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_invitation_full(self):
    """ Tests creating themed invitation cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_invitation_full")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_thankyou_full(self):
    """ Tests creating fully customizable thank-you cards. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_thankyou_full")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 12)

  def test_envelope(self):
    """ Tests creating envelopes. """
    recipient_file = os.path.join(self.DATA_FOLDER, "example_recipients.csv")
    output_path = os.path.join(self.test_dir, "result.pdf")
    input_dir = os.path.join(self.DATA_FOLDER, "example_envelope")
    args = setup_args(recipient_file, input_dir, output_path)

    run(args, lambda _: None)

    self.assert_pdf(output_path, 6)


if __name__ == '__main__':
  unittest.main()
