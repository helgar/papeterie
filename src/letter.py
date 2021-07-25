#!/usr/bin/python3

""" Put it all together! """

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path

from configuration import config_from_json

from output import BaseOutputController
from papeterie import create_single_papeterie
from pdflatex import PdfLatex
from snippets import from_file
from simple_template import SimpleTemplate


DEFAULT_DEFAULTS = os.path.join(str(Path.home()), ".papeterie")
DEFAULT_SNIPPETS = "default.pap"


# pylint: disable=redefined-outer-name

def setup_snippets(args, config):
  """ Setup the snippets collection (possibly from default snippets)

  args:
    parsed args
  config: Configuration
    config info

  returns: Snippets
    the assembled snippet collection

  """
  defaults = args.defaults if args.defaults else DEFAULT_DEFAULTS
  default_snippets_file = os.path.join(defaults, DEFAULT_SNIPPETS)
  if os.path.exists(default_snippets_file):
    default_snippets = from_file(
        config.snippets.keys(), default_snippets_file, check_completeness=False)
  else:
    logging.info("No default snippets file found.")

  snippets = from_file(config.snippets.keys(), args.snippets, check_completeness=False)
  if default_snippets:
    snippets = default_snippets.merge_with(snippets, check_overlapping=False)
  snippets.check_completeness(config.snippets.keys())

  return snippets


def run(args, help_fn):
  """ Do the actual work.

  args:
    commandline arguments
  help_fn: function
    function to call to print help

  """
  output = BaseOutputController(args.output_file)

  print("Log file: %s" % output.log_file)
  logging.basicConfig(filename=output.log_file, filemode='w', level=logging.DEBUG)

  logging.info("Writing output to %s.", output.tmp_dir)

  if not os.path.exists(args.input_dir):
    print("Input directory does not exist: %s" % args.input_dir)
    help_fn()
    sys.exit(1)

  if not os.path.exists(args.snippets):
    print("Snippets file does not exist: %s" % args.snippets)
    help_fn()
    sys.exit(1)

  config = config_from_json(args.input_dir)
  assert config

  tex_template = SimpleTemplate(config.tex_template)
  latex_binary = PdfLatex()
  snippets = setup_snippets(args, config)

  create_single_papeterie(latex_binary, output, tex_template, snippets)

  shutil.copy(output.pdf_path, output.output_file)

  if not args.keep_tmp:
    shutil.rmtree(output.tmp_dir)

# pylint: enable=redefined-outer-name

if __name__ == "__main__":
  # pylint: disable=invalid-name
  parser = argparse.ArgumentParser(description='Load recipients from CSV file.')
  parser.add_argument(
      '--input_dir', type=str, dest="input_dir", required=True,
      help='directory with all input files')
  parser.add_argument(
      '--snippets', type=str, dest="snippets", required=True,
      help='file with snippets')
  parser.add_argument(
      '--output_file', type=str, dest="output_file", required=True,
      help='name of the output file')
  parser.add_argument(
      '--keep-tmp', dest="keep_tmp", default=False, action="store_true",
      help='Whether to keep the temporary files.')
  parser.add_argument(
      '--defaults', dest="defaults", default=None, required=False,
      help='Directory with defaults.')
  # pylint: disable=invalid-name

  args = parser.parse_args()
  run(args, parser.print_help)
