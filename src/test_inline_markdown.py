
import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(
        [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ],
        matches
    )

    def test_extract_double_image(self):
        matches = extract_markdown_images(
            "These images are the same ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/zjjcJKZ.png")
            ],
            matches
        )

    def test_extract_random_brackets(self):
        matches = extract_markdown_images(
            "This is [not alt text] but this is ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png")
            ],
            matches
        )

    def test_extract_only_image(self):
        matches = extract_markdown_images(
            "There is a [link](https://www.wikipedia.org) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png")
            ],
            matches
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        matches = extract_markdown_links(
            "This is a single link [click to go to wikipedia](https://www.wikipedia.org)"
        )
        self.assertEqual(
            [
                ("click to go to wikipedia", "https://www.wikipedia.org")
            ],
            matches
        )

    def test_extract_double_links(self):
        matches = extract_markdown_links(
            "These are two links [click to go to wikipedia](https://www.wikipedia.org) and [click to go to encyclopedia](https://www.britannica.com)"
        )
        self.assertEqual(
            [
                ("click to go to wikipedia", "https://www.wikipedia.org"),
                ("click to go to encyclopedia", "https://www.britannica.com")
            ],
            matches
        )

    def test_extract_random_brackets(self):
        matches = extract_markdown_links(
            "This is not a link [click to go to wikipedia] but this is [click to go to wikipedia](https://www.wikipedia.org)"
        )
        self.assertEqual(
            [
                ("click to go to wikipedia", "https://www.wikipedia.org")
            ],
            matches
        )

    def test_extract_only_link(self):
        matches = extract_markdown_links(
            "There is a [link](https://www.wikipedia.org) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(
            [
                ("link", "https://www.wikipedia.org")
            ],
            matches
        )


if __name__ == "__main__":
    unittest.main()