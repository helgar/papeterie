#/bin/python3

""" Provides a reusable jinja template, that renders text given a recipient. """

from jinja2 import Template


# pylint: disable=too-few-public-methods

class JinjaTemplate():
  """ Wrapper for a jinja2 template to be reused by several recipients.

  template_path: string
    path of the jinja template file

  """

  def __init__(self, template_path):
    with open(template_path, 'r', encoding='utf-8') as infile:
      template_str = u"".join(infile.readlines())
    self.__template = Template(template_str)

  def render(self, recipient):
    """ Renders the template with the data of the recipient.

    recipient: Recipient
      a recipient's data

    returns: string
      the rendered text

    """
    return self.__template.render(**recipient.to_dict())

# pylint: enable=too-few-public-methods
