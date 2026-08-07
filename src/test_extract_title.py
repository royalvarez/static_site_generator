
import unittest

from extract_title import extract_title


class TestExtractTitleMarkdown(unittest.TestCase):
    def test_single_line(self):
        markdown = """
# This is our world
"""
        title = extract_title(markdown)
        self.assertEqual(
            "This is our world",
            title
        )


    def test_multiple_lines(self):
        markdown = """
# Welcome to LOTR

Aragorn rushes through the forest
ducking low to remain out of sight

Orcs marching westward to Riverdale
dragging Frodo and Sam along
"""
        title = extract_title(markdown)
        self.assertEqual(
            "Welcome to LOTR",
            title
        )


if __name__ == "__main__":
    unittest.main()
