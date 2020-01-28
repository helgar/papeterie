#/bin/python3

""" Put it all together! """

import argparse
import logging
import os
import shutil
import sys

from configuration import config_from_json
from csv2recipients import load_recipients
from jinja2snippet import JinjaTemplate
from output import SerialOutputController
from papeterie import create_single_papeterie
from pdflatex import PdfLatex
from pdf import merge_pdfs
from snippets import Snippets, PAPETERIEPICPATH
from simple_template import SimpleTemplate
from gpg import Signer


# pylint: disable=redefined-outer-name

def run(args, help_fn):
  """ Do the actual work.

  args:
    commandline arguments
  help_fn: function
    function to call to print help

  """
  output = SerialOutputController(args.output_file)

  print("Log file: %s" % output.log_file)
  logging.basicConfig(filename=output.log_file, filemode='w', level=logging.DEBUG)

  logging.info("Writing output to %s.", output.tmp_dir)

  if not os.path.exists(args.recipient_file):
    print("Recipient file does not exist: %s" % args.recipient_file)
    help_fn()
    sys.exit(1)

  if not os.path.exists(args.input_dir):
    print("Input dir does not exist: %s" % args.input_dir)
    help_fn()
    sys.exit(1)

  config = config_from_json(args.input_dir)
  assert config
  if config.signed_snippets and not args.gpg_key:
    print("The config contains snippets to sign, but no GPG key was specified.")
    help_fn()
    sys.exit(1)

  recipients = load_recipients(args.recipient_file)
  tex_template = SimpleTemplate(config.tex_template)
  latex_binary = PdfLatex()
  signer = Signer(output.tmp_dir, args.gpg_key, args.gpg_homedir)
  jinja_templates = {name: JinjaTemplate(template)
                     for (name, template) in config.snippets.items()}

  idx = 0
  for recipient in recipients:
    logging.info("Processing recipient idx %s.", idx)
    logging.info(recipient)

    idx_output = output.get_indexed_output_controller(idx)

    snippets = Snippets({snippet: jinja_templates[snippet].render(recipient)
                         for snippet in config.snippets})

    # Set a special snippet so that the picture files are correctly referenced.
    snippets = snippets.add(PAPETERIEPICPATH, args.input_dir)

    if config.signed_snippets:
      signed_snippets = snippets \
        .subset(config.signed_snippets.values()) \
        .renamed({v: k for (k, v) in config.signed_snippets.items()}) \
        .transform(signer.sign)

      snippets = snippets.merge_with(signed_snippets)

    create_single_papeterie(
        latex_binary, idx_output, tex_template, snippets)

    idx += 1

  merge_pdfs(output.pdf_pattern, output.pdf_path)

  shutil.copy(output.pdf_path, output.output_file)

  if not args.keep_tmp:
    shutil.rmtree(output.tmp_dir)

# pylint: enable=redefined-outer-name


if __name__ == "__main__":
  # pylint: disable=invalid-name
  parser = argparse.ArgumentParser(description='Create beautiful and secure serial papeterie.')
  parser.add_argument(
      '--recipient_file', type=str, dest="recipient_file", required=True,
      help='file with recipient data')
  parser.add_argument(
      '--input_dir', type=str, dest="input_dir", required=True,
      help='directory with all input files')
  parser.add_argument(
      '--gpg-key', type=str, dest="gpg_key", required=False,
      help='Key ID of a GPG key to sign text snippets.')
  parser.add_argument(
      '--output_file', type=str, dest="output_file", required=True,
      help='name of the output file')
  parser.add_argument(
      '--keep-tmp', dest="keep_tmp", default=False, action="store_true",
      help='Whether to keep the temporary files.')
  parser.add_argument(
      '--gpg-homedir', type=str, dest="gpg_homedir", required=False,
      help='Key ID of a GPG key to sign text snippets.')
  args = parser.parse_args()
  # pylint: enable=invalid-name

  run(args, parser.print_help)
