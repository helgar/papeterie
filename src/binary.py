#/bin/python3

""" Module to run an external binary on the shell. """

import logging
import subprocess

class BinaryException(Exception):
  """ Exceptions of this module. """


def run_cmd(cmd):
  """ Runs the command in the shell.

  Returns:
    (stdout, stderr, returncode)

  """
  completed_process = None

  try:
    completed_process = subprocess.run(cmd, shell=True, check=False, capture_output=True)
    logging.info(completed_process)
  except:
    raise BinaryException(
        "Running command failed: %s." % cmd)

  if not completed_process.returncode == 0:
    logging.warning("Process exited with non-zero return code.")

  return (completed_process.stdout, completed_process.stderr, completed_process.returncode)


class Binary:
  """ Representing an external binary. """
  # pylint: disable=too-few-public-methods

  def __init__(self, name):
    self.__name = name
    self.__check_installation()

  def __check_installation(self):
    cmd = "which %s" % self.__name
    (_, _, code) = run_cmd(cmd)
    if code:
      raise BinaryException(
          "The binary %s does not exist on this system. Please install it." % self.__name)

  def run_binary(self, arguments):
    """ Runs the binary with the given arguments.

    arguments: string
      string with arguments

    returns: (str, str, str)
      tuple of (out, err, code), where out is the output of the call on STDOUT,
      err on STDERR, and code is the return code.

    """
    cmd = "%s %s" % (self.__name, arguments)
    logging.info("Running command: %s", cmd)
    (out, err, code) = run_cmd(cmd)
    logging.info("Stdout: %s", out)
    logging.info("Stderr: %s", err)
    logging.info("Return code: %s", code)
    if code:
      raise BinaryException("Running command %s failed." % cmd)
    return (out, err, code)

  # pylint: enable=too-few-public-methods
