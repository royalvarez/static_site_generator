
import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type


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


class TestBlockToBlockType(unittest.TestCase):
    def test_block_headings(self):
        block = "# Welcome to the world of tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
        block = "## Welcome to the world of double tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
        block = "### Welcome to the world of triple tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
        block = "#### Welcome to the world of quadruple tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
        block = "##### Welcome to the world of quintuple tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
        block = "###### Welcome to the world of sextuple tomorrow!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )

    def test_block_code(self):
        block = "```\nrank = 1\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.CODE,
            block_type
        )

    def test_block_quote(self):
        block = "> Execute order 66"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.QUOTE,
            block_type
        )

    def test_block_list(self):
        block = "- I do not like order"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.ULIST,
            block_type
        )
        block = "1. I do like order\n2. Down with the rebellion"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.OLIST,
            block_type
        )

    def test_block_paragraph(self):
        block = "Paragraph gon wild"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )
        block = "```\nI never closed my code block..."
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )
        block = "> I try to follow quoting standards\nbut i much prefer to cause mischief"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )
        block = "- I do not like order\n I execute aall orders causing chaos and failing unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )

        block = "1. I do like order\n66. I execute aall orders causing chaos and failing order list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )


if __name__ == "__main__":
    unittest.main()