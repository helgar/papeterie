#/bin/python3

""" Module to merge several pdfs into one. """

import glob
from PyPDF2 import PdfFileWriter, PdfFileReader


def merge_pdfs(pattern, output_path):
  """ Merge several PDFs into one.

  pattern: string
    pattern to list all files to merge
  output_path: string
    path of the output file

  """
  writer = PdfFileWriter()

  paths = glob.glob(pattern)

  for path in paths:
    reader = PdfFileReader(path)
    for page in range(reader.getNumPages()):
      writer.addPage(reader.getPage(page))

  with open(output_path, 'wb') as outfile:
    writer.write(outfile)
