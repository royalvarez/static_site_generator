
import unittest

from htmlnode import HTMLNode, LeafNode


class test_HTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode('b', "most", None, None)
        self.assertRaises(NotImplementedError, node. to_html)

    def test_props_html(self):
        node = HTMLNode(
            "a",
            "the Google browser",
            None,
            {"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(
            " href=\"https://google.com\" target=\"_blank\"",
            node.props_to_html()
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "The master of Kenobi",
            None,
            {"class": "history"}
        )

        self.assertEqual(
            "div",
            node.tag
        )
        self.assertEqual(
            "The master of Kenobi",
            node.value
        )
        self.assertEqual(
            None,
            node.children
        )
        self.assertEqual(
            {"class": "history"},
            node.props
        )

    def test_repr(self):
        node = HTMLNode("h1", "The wonderful browser is Google", None, None)
        self.assertEqual(
            "HTMLNode(h1, The wonderful browser is Google, None, None)",
            repr(node)
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode('p', "Hello, world!")
        self.assertEqual(
            "<p>Hello, world!</p>",
            node.to_html()
        )

    def test_leaf_to_html_a(self):
        node = LeafNode('a', "Click me", {"href": "https://boot.dev"})
        self.assertEqual(
            "<a href=\"https://boot.dev\">Click me</a>",
            node.to_html()
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Contents", {"class": "main"})
        self.assertEqual(
            "<h1 class=\"main\">Contents</h1>",
            node.to_html()
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "A tagless world.")
        self.assertEqual(
            "A tagless world.",
            node.to_html()
        )

    def test_repr(self):
        node = LeafNode('p', "Hello, world!")
        self.assertEqual(
            "LeafNode(p, Hello, world!, None)",
            repr(node)
        )


if __name__ == "__main__":
    unittest.main()