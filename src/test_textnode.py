import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("Link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Text node", TextType.ITALIC)

        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Text", TextType.TEXT)

        self.assertEqual(repr(node), "TextNode(Text, text, None)")

    def test_conversion_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
