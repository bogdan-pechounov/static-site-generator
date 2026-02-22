import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TextHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="p",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        self.assertEqual(HTMLNode().props_to_html(), "")
        self.assertEqual(HTMLNode(props={}).props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello there", None, {"id": "2"})

        self.assertEqual(repr(node), "HTMLNode(p, Hello there, None, {'id': '2'})")

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "This is a paragraph of text.")

    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_node_with_attributes(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
