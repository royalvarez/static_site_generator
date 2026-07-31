
import unittest

from inline_markdown import split_nodes_delimiter

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("I am partially **bolded**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("I am partially ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delimiter_bold_double(self):
        node = TextNode("I am **bold** and I am **bold2** as well", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("I am ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and I am ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" as well", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_bold_multiple_word(self):
        node = TextNode("I have **bold word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("I have ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delimiter_italic(self):
        node = TextNode("I am _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("I am ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delimiter_bold_and_italic(self):
        node = TextNode("I am **bold** and I am _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("I am ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and I am ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delimiter_code(self):
        node = TextNode("I am a ```code``` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "```", TextType.CODE)
        self.assertEqual(
            [
                TextNode("I am a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" block", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_unmatch(self):
        node = TextNode("```I am an opened code block", TextType.TEXT)
        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            [node],
            "```",
            TextType.CODE
        )


if __name__ == "__main__":
    unittest.main()