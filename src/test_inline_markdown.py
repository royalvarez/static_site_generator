
import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image_start(self):
        nodes = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png",),
            ],
            new_nodes
        )


    def test_split_single_image_middle(self):
            nodes = TextNode(
            "This is a single ![image](https://i.imgur.com/zjjcJKZ.png) in between text",
            TextType.TEXT
        )
            new_nodes = split_nodes_image([nodes])
            self.assertEqual(
                [
                    TextNode("This is a single ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png",),
                    TextNode(" in between text", TextType.TEXT)
                ],
                new_nodes
            )


    def test_split_single_image_end(self):
            nodes = TextNode(
            "This is a single at the end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
            new_nodes = split_nodes_image([nodes])
            self.assertEqual(
                [
                    TextNode("This is a single at the end ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png",)
                ],
                new_nodes
            )


    def test_split_double_image_start_end(self):
        nodes = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(' ', TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )


    def test_split_image_start_middle(self):
        nodes = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png) is in between text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" is in between text", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_image_middle_end(self):
        nodes = TextNode(
            "This is in between text ![image](https://i.imgur.com/zjjcJKZ.png) and this is at the end ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])
        self.assertEqual(
            [
                TextNode("This is in between text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and this is at the end ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link_start(self):
        nodes = TextNode(
            "[link](https://boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([nodes])
        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            new_nodes
        )


    def test_split_single_link_middle(self):
        nodes = TextNode(
            "This is [link](https://boot.dev) in between text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([nodes])
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" in between text", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_single_link_end(self):
            nodes = TextNode(
            "This is a single at the end [link](https://boot.dev)",
            TextType.TEXT
        )
            new_nodes = split_nodes_link([nodes])
            self.assertEqual(
                [
                    TextNode("This is a single at the end ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev")
                ],
                new_nodes
            )


    def test_split_double_image_start_end(self):
        nodes = TextNode(
            "[link](https://boot.dev) [second link](https://youtube.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([nodes])
        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(' ', TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com")
            ],
            new_nodes
        )


    def test_split_image_start_middle(self):
        nodes = TextNode(
            "[link](https://boot.dev) and [second link](https://youtube.com) is in between text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([nodes])
        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com"),
                TextNode(" is in between text", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_image_middle_end(self):
        nodes = TextNode(
            "This is in between text [link](https://boot.dev) and this is at the end [second link](https://youtube.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([nodes])
        self.assertEqual(
            [
                TextNode("This is in between text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and this is at the end ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com")
            ],
            new_nodes
        )



if __name__ == "__main__":
    unittest.main()