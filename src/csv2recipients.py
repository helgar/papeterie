#/bin/python3

""" Module to load a list of recipients from a CSV file. """

import csv
import logging

from recipient import Recipient


class Csv2RecipientsException(Exception):
  """ Exceptions for this module. """


def load_recipients(filename):
  """ Reads a CSV file and creates a list of recipients. """
  recipients = []
  with open(filename, newline='') as csvfile:
    recipients_reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    is_headerline = True
    headerline = None

    for recipient in recipients_reader:
      if is_headerline:
        headerline = recipient
        is_headerline = False
        continue
      recipients.append(Recipient(headerline, recipient))

  if is_headerline:
    raise Csv2RecipientsException("No lines found.")

  if not recipients:
    raise Csv2RecipientsException("No data lines found.")

  logging.info("Loaded %d recipients with %d fields.", len(recipients), len(headerline))

  return recipients
