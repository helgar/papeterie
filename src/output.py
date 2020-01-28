#/bin/python3

""" Module for output controllers.

Output controllers compose the various temporary and final filenames in a
consistent manner.

"""

import os
import tempfile


class OutputControllerException(Exception):
  """ Exceptions of this module. """


class BaseOutputController():
  """ Base class for output controllers.

  output_file: string
    path of the final output file (pdf).
  tmp_dir: string (optional)
    the path of a directory to write temporary files in

  """
  def __init__(self, output_file, tmp_dir=None):
    self.__tmp_dir = tmp_dir
    if not self.__tmp_dir:
      self.__tmp_dir = tempfile.mkdtemp()
    self.__output_file = output_file

  @property
  def log_file(self):
    """ Log file of the entire script. """
    return os.path.join(self.__tmp_dir, "main.log")

  @property
  def tmp_dir(self):
    """ Directory to write temporary files in.

    Will be deleted after script execution if --keep-tmp is specified.

    """
    return self.__tmp_dir

  @property
  def output_file(self):
    """ Filename of the final output file (pdf). """
    return self.__output_file

  @property
  def tex_collection(self):
    """ Filename of the collection of tex snippets. """
    return os.path.join(self.__tmp_dir, "tex_collection.txt")

  @property
  def tex_result(self):
    """ Filename of the assembled tex file to be compiled to the final pdf. """
    return os.path.join(self.__tmp_dir, "papeterie.tex")

  @property
  def pdf_basename(self):
    """ Basename of the final pdf file. """
    # pylint: disable=no-self-use
    return "papeterie"

  @property
  def pdf_path(self):
    """ Path of the pdf file in the temporary directory. """
    return os.path.join(self.__tmp_dir, "%s.pdf" % self.pdf_basename)


class IndexedOutputController(BaseOutputController):
  """ Output controller which produces filenames with a given index in the filenames.

  This is used for creating the individual pdfs which are later composed to one final
  pdf.

  output_file: see BaseOutputController
  tmp_dir: see BaseOutputController
  idx: integer
    number of the piece of papeterie in the whole series

  """
  def __init__(self, output_file, tmp_dir, idx):
    if not tmp_dir:
      raise OutputControllerException(
          "The indexed output controller requires a temp dir.")
    super().__init__(output_file, tmp_dir=tmp_dir)
    self.__idx = idx

  def get_snippet_file(self, name):
    """ Filename of a single file containing a specific snippet.

    name: string
      name of the snippet

    """
    return os.path.join(self.tmp_dir,
                        "snippet_%s_%03d.txt" % (name.lower(), self.__idx))

  @property
  def snippet_collection(self):
    """ Filename of the text file containing all snippets for one piece of papeterie. """
    return os.path.join(self.tmp_dir, "snippet_collection_%03d.txt" % self.__idx)

  @property
  def tex_collection(self):
    """ Filename of the texified snippet collection. """
    return os.path.join(self.tmp_dir, "tex_collection_%03d.txt" % self.__idx)

  @property
  def tex_result(self):
    """ Filename of the assembled tex file ready to be compiled to pdf. """
    return os.path.join(self.tmp_dir, "result_%03d.tex" % self.__idx)

  @property
  def pdf_basename(self):
    # pylint: disable=no-self-use
    return "papeterie_%03d" % self.__idx

  @property
  def pdf_path(self):
    return os.path.join(self.tmp_dir, "%s.pdf" % self.pdf_basename)


class SerialOutputController(BaseOutputController):
  """ Manages the output files for a papeterie composed of a series of pieces.

  output_file:
    file name of the output file
  timestamp:
    boolean, indicating whether or not a subfolder named like a timestamp should be created.
    This is useful when you want to render the same papeterie several times and want to keep
    all results.

  """

  def __init__(self, output_file):
    super().__init__(output_file)

  @property
  def pdf_pattern(self):
    """ Regex pattern to collect all pdfs of all pieces of papeterie.

    idx: int
      index of the piece of papeterie

    """
    return os.path.join(self.tmp_dir, "papeterie_*.pdf")

  def get_indexed_output_controller(self, idx):
    """ Returns an output controller for an indivdual numbered piece of papeterie.

    idx: integer
      number of the piece of papeterie

    """
    return IndexedOutputController(self.output_file, self.tmp_dir, idx)
