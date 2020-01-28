#!/usr/bin/python3

""" Unit tests for binary. """

import shutil
import tempfile
import unittest

from testing import PapeterieTestCase
from binary import run_cmd, Binary, BinaryException


class TestRunCmd(PapeterieTestCase):
  """ Tests the run_cmd function of the binary module. """

  def test_run_cmd_success(self):
    """ Test running a command. """
    cmd = "true"

    (out, err, code) = run_cmd(cmd)

    self.assertFalse(out)
    self.assertFalse(err)
    self.assertEqual(0, code)

  def test_run_cmd_success_output(self):
    """ Test running a command. """
    cmd = "echo cat"

    (out, err, code) = run_cmd(cmd)

    self.assertEqual(b"cat\n", out)
    self.assertFalse(err)
    self.assertEqual(0, code)

  def test_run_cmd_fail(self):
    """ Test running a failing command. """
    cmd = "false"

    (out, err, code) = run_cmd(cmd)

    self.assertFalse(out)
    self.assertFalse(err)
    self.assertGreater(code, 0)

  def test_run_cmd_fail_output(self):
    """ Test running a failing command with output on stderr. 1"""
    cmd = "ls /tmp/doesnotexist"

    (out, err, code) = run_cmd(cmd)

    self.assertFalse(out)
    self.assertTrue(err)
    self.assertGreater(code, 0)


class TestBinary(unittest.TestCase):
  """ Tests the Binary class of the binary module. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  # pylint: disable=no-self-use
  def test_check_installation_success(self):
    """ Test testing whether the binary is installed or not. """
    Binary("test")
    # No exception: everything is fine
  # pylint: enable=no-self-use

  def test_check_installation_fail(self):
    """ Test that checking for a non-existing binary fails. """
    with self.assertRaises(BinaryException):
      Binary("notinstalled")


if __name__ == '__main__':
  unittest.main()
