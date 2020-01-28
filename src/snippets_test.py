#!/usr/bin/python3

""" Unit tests for snippets. """

import os
import unittest
import shutil
import tempfile

import snippets
from testing import PapeterieTestCase


# pylint: disable=too-many-public-methods
# It's a complicated class, it warrants many tests

class TestSnippets(PapeterieTestCase):
  """ Test Snippets. """

  def setUp(self):
    self.test_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_valid_snippet(self):
    """ Test creation from dict with valid data. """
    names = ["A", "B", "C"]
    snippet_dict = {"A": "a", "B": "b", "C": "c"}

    snippet_collection = snippets.from_dict(names, snippet_dict)
    self.assertEqual(snippet_dict, snippet_collection.to_dict())

  def test_snippet_overlap(self):
    """ Test creation from dict with valid data. """
    names = ["A", "BA", "C"]
    snippet_dict = {"A": "a", "BA": "b", "C": "c"}

    with self.assertRaises(snippets.SnippetsException):
      snippets.from_dict(names, snippet_dict)

  def test_to_uppercase(self):
    """ Test creation from dict with valid data. """
    names = ["A", "B", "C"]
    snippet_dict = {"a": "a", "B": "b", "c": "c"}

    snippet_collection = snippets.from_dict(names, snippet_dict)

    expected = {"A": "a", "B": "b", "C": "c"}
    self.assertEqual(expected, snippet_collection.to_dict())

  def test_superfluous_snippet(self):
    """ Test creation from dict with more data than necessary. """
    names = ["A", "B", "C"]
    snippet_dict = {"A": "a", "B": "b", "C": "c", "D": "d"}

    snippet_collection = snippets.from_dict(names, snippet_dict)
    self.assertEqual(snippet_dict, snippet_collection.to_dict())

  def test_no_names(self):
    """ Test creation from dict with no names. """
    names = []
    snippet_dict = {"A": "a"}

    with self.assertRaises(snippets.SnippetsException):
      snippets.from_dict(names, snippet_dict)

  def test_no_snippets(self):
    """ Test creation from dict with no snippets """
    names = ["A", "B", "C"]
    snippet_dict = {}

    with self.assertRaises(snippets.SnippetsException):
      snippets.from_dict(names, snippet_dict)

  def test_missing_snippets(self):
    """ Test creation from dict with a missing snippet """
    names = ["A", "B", "C"]
    snippet_dict = {"A": "a", "C": "c"}

    with self.assertRaises(snippets.SnippetsException):
      snippets.from_dict(names, snippet_dict)

  def test_str(self):
    """ Tests generating the string representaiton of a snippets instance. """
    snippet_collection = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    self.assertEqual("A\na\nB\nb\nC\nc\n", str(snippet_collection))

  def test_transform(self):
    """ Tests creating snippet collections from other snippet collections. """
    original = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    new = original.transform()

    self.assertEqual(original.to_dict(), new.to_dict())

  def test_from_snippets_string(self):
    """ Tests creating snippet collection from a raw snippet string. """
    names = ["A", "B", "C"]
    snippet_string = "A\na\nC\nc\nB\nb"

    result = snippets.from_snippets_string(names, snippet_string)

    expected = {"A": "a", "C": "c", "B": "b"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_snippets_subset(self):
    """ Tests creating a snippet collection that is a subset of another one. """
    original = snippets.Snippets({"A": "a", "C": "c", "B": "b"})

    result = original.subset(["A", "C"])

    expected = {"A": "a", "C": "c"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_snippets_renamed(self):
    """ Tests creating a snippet collection that is a renamed version of another. """
    original = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    name_map = {"A": "X", "B": "B", "C": "Z"}

    result = original.renamed(name_map)

    expected = {"X": "a", "B": "b", "Z": "c"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_merged_snippets(self):
    """ Tests creating a snippet collection from two other collections. """
    original1 = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    original2 = snippets.Snippets({"X": "x", "Y": "y", "Z": "z"})

    result = original1.merge_with(original2)

    expected = {"A": "a", "B": "b", "C": "c", "X": "x", "Y": "y", "Z": "z"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_merged_snippets_overlapping_forbidden(self):
    """ Tests creating a snippet collection from two other collections. """
    original1 = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    original2 = snippets.Snippets({"B": "x", "Y": "y", "Z": "z"})

    with self.assertRaises(snippets.SnippetsException):
      original1.merge_with(original2)

  def test_from_merged_snippets_overlapping_allowed(self):
    """ Tests creating a snippet collection from two other collections. """
    original1 = snippets.Snippets({"A": "a", "C": "c", "B": "b"})
    original2 = snippets.Snippets({"B": "x", "Y": "y", "Z": "z"})

    result = original1.merge_with(original2, check_overlapping=False)

    expected = {"A": "a", "B": "x", "C": "c", "Y": "y", "Z": "z"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_file(self):
    """ Test creation from files. """
    snippet_file_content = "A\na\nB\nb\nC\nc"
    snippet_file_path = os.path.join(self.test_dir, "snippets")
    with open(snippet_file_path, 'w') as outfile:
      outfile.write(snippet_file_content)
    snippet_names = ["A", "B", "C"]

    result = snippets.from_file(snippet_names, snippet_file_path)

    expected = {"A": "a", "B": "b", "C": "c"}
    self.assertEqual(result.to_dict(), expected)

  def test_from_file_completeness_fail(self):
    """ Test creation from files. """
    snippet_file_content = "A\na\nC\nc"
    snippet_file_path = os.path.join(self.test_dir, "snippets")
    with open(snippet_file_path, 'w') as outfile:
      outfile.write(snippet_file_content)
    snippet_names = ["A", "B", "C"]

    with self.assertRaises(snippets.SnippetsException):
      snippets.from_file(snippet_names, snippet_file_path)

  def test_from_file_no_completeness_check(self):
    """ Test creation from files. """
    snippet_file_content = "A\na\nC\nc"
    snippet_file_path = os.path.join(self.test_dir, "snippets")
    with open(snippet_file_path, 'w') as outfile:
      outfile.write(snippet_file_content)
    snippet_names = ["A", "B", "C"]

    result = snippets.from_file(snippet_names, snippet_file_path, check_completeness=False)

    expected = {"A": "a", "C": "c"}
    self.assertEqual(result.to_dict(), expected)

  def test_add_snippet(self):
    """ Test creation from dict with valid data. """
    snippet_dict = {"A": "a", "B": "b", "C": "c"}
    original = snippets.Snippets(snippet_dict)

    result = original.add("X", "x")

    expected = {"A": "a", "B": "b", "C": "c", "X": "x"}
    self.assertEqual(expected, result.to_dict())

# pylint: enable=too-many-public-methods


if __name__ == '__main__':
  unittest.main()
