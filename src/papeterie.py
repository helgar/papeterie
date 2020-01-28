#/bin/python3

""" Common high level code of all papeterie types. """

import logging

from tex import texify


def create_single_papeterie(pdflatex, output, template, snippets):
  """ Creates one single file of papeterie.

  pdflatex: PdfLatex
    the binary that compiles the pdf
  output: BaseOutputController
    a thing that knows all the filenames
  template: SimpleTemplate
    a simple template with placeholders
  snippets: Snippets
    a collection of snippets that fit the placeholders of the template

  """
  texified_snippets = snippets.transform(texify)
  texcontent = template.render(texified_snippets)
  with open(output.tex_result, 'w') as outfile:
    outfile.write(texcontent)
  logging.info("Wrote tex file %s.", output.tex_result)

  pdflatex.run(
      output.tmp_dir,
      output.pdf_basename,
      output.tex_result)
  logging.info("Wrote pdf %s.", output.pdf_path)
