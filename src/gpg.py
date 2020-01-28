#/bin/python3

""" Module to GPG-sign a file. """

import os
import re
import tempfile
import textwrap
from pathlib import Path

from binary import Binary

# Note: There is a gnupg-python library, but it does not support gpg (as of Jan 2020)


class Gpg2Exception(Exception):
  """ Exception being thrown in this module. """


class Gpg2(Binary):
  """ The gpg2 binary.

  homedir: string
    path of the GPG2 home directory.

  """

  # pylint: disable=anomalous-backslash-in-string
  KEY_PATTERN = b"\s*(?P<keyid>\S+)\n.*"
  # pylint: enable=anomalous-backslash-in-string
  KEY_ID = "keyid"

  def __init__(self, homedir=None):
    super().__init__("gpg2")
    if not homedir:
      self.__homedir = os.path.join(str(Path.home()), ".gnupg")
    else:
      self.__homedir = homedir

  @property
  def homedir(self):
    """ The gpg2's home directory.

    In most cases this will be ".gnupg" in the user's home directory. However, here
    it is customizable, for example for testing.

    """
    return self.__homedir

  def get_keyid(self, email):
    """ Gets the key ID for the key belonging to the given email address.

    Note: this probably fails horribly if there is more than one key with that address.

    email: string
      email address belonging to a key

    returns: string
      the key's ID

    """
    args = "--homedir=%s --list-secret-keys | grep -B 1 %s" % (self.__homedir, email)
    (out, _, code) = self.run_binary(args)
    if code:
      raise Gpg2Exception("Generated key not found.")

    return re.search(self.KEY_PATTERN, out).group(self.KEY_ID).decode("utf-8")

  def generate_key(self, instructions_file):
    """ Generates a key in a temporary home dir.

    Only to be used for unit tests.

    instructions_file: string
      path of an instructions file for batch generation of a key

    """
    args = "--homedir=%s --batch --generate-key %s" % (self.__homedir, instructions_file)
    (_, _, code) = self.run_binary(args)
    if code:
      raise Gpg2Exception("Key generation failed.")

  def sign_file(self, infile, key_id):
    """ Signs a file with the given key.

    infile: string
      path of file to be signed
    key_id: string
      ID of the key to use for signing

    """
    args = "--homedir=%s --armor --clearsign --local-user %s %s" % (
        self.__homedir, key_id, infile)
    (_, _, code) = self.run_binary(args)
    if code:
      raise Gpg2Exception("Signing file %s with key %id failed." % (infile, key_id))

  def check_signature(self, infile):
    """ Checks that the given file contains a valid GPG signature.

    infile: string
      path of the file containing the signed message

    raises: Gpg2Exception
      when the signature is not a good one

    """
    args = "--homedir=%s --verify %s" % (self.__homedir, infile)
    (_, _, code) = self.run_binary(args)
    if code:
      raise Gpg2Exception("The signature of file %s could not be verified." % infile)


class Signer:
  # pylint: disable=too-few-public-methods
  """ Class to provide a simple 'sign' method for texts.

  tmp_dir: string
    path of a directory to store temporary files in
  key_id: string
    ID of the GPG key to use for signing
  gpg_homedir: string
    path of the GPG homedir

  """

  LEN_SIGNATURE = 64

  def __init__(self, tmp_dir, key_id, gpg_homedir=None):
    self.__gpg = Gpg2(homedir=gpg_homedir)
    self.__key_id = key_id
    self.__tmp_dir = tmp_dir
    self.__wrapper = textwrap.TextWrapper(width=self.LEN_SIGNATURE, replace_whitespace=False)

  def sign(self, intext):
    """ Sign given text file.

    intext: string
      text to be signed

    """
    infile_path = tempfile.NamedTemporaryFile(dir=self.__tmp_dir)
    # The text is wrapped at the width of the signature, as otherwise it is line-broken
    # at arbitrary positions that make signature verification impossible.
    intext = "\n".join(self.__wrapper.wrap(text=intext))
    with open(infile_path.name, 'w') as infile:
      infile.write(intext)

    self.__gpg.sign_file(infile.name, self.__key_id)

    outfile_path = os.path.join(self.__tmp_dir, "%s.asc" % infile.name)
    with open(outfile_path, 'r', encoding='utf-8') as outfile:
      outtext = u"".join(outfile.readlines())

    return outtext
  # pylint: enable=too-few-public-methods
