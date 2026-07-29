
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span>child</span></div>",
            parent_node.to_html()
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode('b', "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span><b>grandchild</b></span></div>",
            parent_node.to_html()
        )

    def test_to_html_with_nested_parents(self):
        item1 = LeafNode("li", "dog food")
        item2 = LeafNode("li", "cat food")
        grandchild_node = ParentNode("ol", [item1, item2], {"class": "important"})
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"class": "primary"})
        self.assertEqual(
            "<div class=\"primary\"><h1><ol class=\"important\"><li>dog food</li><li>cat food</li></ol></h1></div>",
            parent_node.to_html()
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(
            ValueError,
            parent_node.to_html
        )

    def test_to_html_with_many_children(self):
        children = [LeafNode("li", "Bank of China", {"class": "Asia"}), LeafNode("li", "Bank of America")]
        parent_node = ParentNode('ul', children, {"class": "important"})
        self.assertEqual(
            "<ul class=\"important\"><li class=\"Asia\">Bank of China</li><li>Bank of America</li></ul>",
            parent_node.to_html()
        )

    def test_to_html_heading(self):
        parent_node = ParentNode(
            "h1",
            [
                LeafNode('b', "Most bold"),
                LeafNode(None, "and"),
                LeafNode('i', "Most italic"),
                LeafNode(None, "man")
            ],
        )
        self.assertEqual(
            "<h1><b>Most bold</b>and<i>Most italic</i>man</h1>",
            parent_node.to_html()
        )



if __name__ == "__main__":
    unittest.main()