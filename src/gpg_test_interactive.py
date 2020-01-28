#!/usr/bin/python3

""" Unit tests for texfile. """

import os
import shutil
import tempfile
import unittest

from testing import PapeterieTestCase, setup_gpg


class TestGpg(PapeterieTestCase):
  """ Tests the gpg module.

  Note: running this, you will be prompted for a passphrase. Type in 'Test123'.

  Technically speaking, this is not a unit test, because it requires human
  interaction. This is on purpose, because otherwise it does not test the
  reality. Think of it more like an integration test.

  For running the papeterie scripts including signing passages, we require
  a real GPG key being setup properly, with an actual passphrase that the user
  has to type. (Repeated input of passphrases for several passages can be
  simplified by using a gpg-atent.)

  If the unit test would automate the input of the passphrase by a user, it would
  be tempting for the user to use the same mechanism of using a test key
  for the signature instead of setting up a real one. We want to encourage proper
  usage of GPG infrastructure and therefore don't offer automation here.

  """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()
    (self.gpg, self.key) = setup_gpg(self.test_dir, self.TESTDATA_FOLDER)

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_sign(self):
    """ Test signing a file. """
    infile_orig = os.path.join(self.TESTDATA_FOLDER, "snippet1.txt")
    infile = os.path.join(self.test_dir, "file.txt")
    shutil.copy(infile_orig, infile)
    self.assertTrue(os.path.exists(infile))

    self.gpg.sign_file(infile, self.key)

    self.assertTrue(os.path.exists(infile + ".asc"))


if __name__ == '__main__':
  unittest.main()
