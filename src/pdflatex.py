#/bin/python3

""" Module to create a pdf from a tex file. """

import os

from binary import Binary


class PdfLatexException(Exception):
  """ Exception for this module. """

class PdfLatex(Binary):
  """ The 'pdflatex' binary. """

  def __init__(self):
    super().__init__("pdflatex")

  def run(self, out_dir, out_basename, filename):
    """ Compiles a pdf from a tex file.

    out_dir: string
      path of the output directory
    out_basename: string
      basename of the pdf output file
    filename: string
      path of the input tex file

    """
    if not os.path.exists(filename):
      raise PdfLatexException("The input file %s does not exist." % filename)

    args = "-output-directory=%s -jobname=%s %s" % (out_dir, out_basename, filename)
    super().run_binary(args)

    expected_output = os.path.join(out_dir, "%s.pdf" % out_basename)
    if not os.path.exists(expected_output):
      raise PdfLatexException("Ooops, no pdf was generated here: %s" % expected_output)
