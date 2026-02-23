import unittest

from genate_html import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        title = extract_title("# Title")
        self.assertEqual(title, "Title")

    def test_multi_line(self):
        md = """
#  Heading

Content
"""
        title = extract_title(md)

        self.assertEqual(title, "Heading")
