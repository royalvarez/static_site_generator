
import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        md = """
> cogito ergo sum
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "> cogito ergo sum"
            ],
            blocks
        )

    def test_multiple_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ],
            blocks
        )

    def test_no_blocks(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [''],
            blocks
        )


if __name__ == "__main__":
    unittest.main()