
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node number 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node with a url", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node without a url", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, link, https://boot.dev)",
            repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        text_node = TextNode("I am the boldest", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "I am the boldest")

    def test_link(self):
        text_node = TextNode("click me", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "click me")
        self.assertEqual(html_node.props, {"href": f"{text_node.url}"})

    def test_image(self):
        text_node = TextNode("alternate text", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": f"{text_node.url}", "alt": f"{text_node.text}"})

    def test_no_type(self):
        text_node = TextNode(None, None)
        self.assertRaises(ValueError, text_node_to_html_node, text_node)


if __name__ == "__main__":
    unittest.main()