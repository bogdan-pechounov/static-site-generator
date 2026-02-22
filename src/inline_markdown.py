import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        # Only process text nodes for delimiters
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        splits = old_node.text.split(delimiter)

        # If the length is even, it means there is an unclosed delimiter
        if len(splits) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i, split in enumerate(splits):
            # Skip empty strings due to delimiters at the start or end
            if not split:
                continue

            # Even indices correspond to text outside delimiters
            if i % 2 == 0:
                new_node = TextNode(text=split, text_type=TextType.TEXT)
            # Odd indices correspond to text inside delimiters
            else:
                new_node = TextNode(text=split, text_type=text_type)

            new_nodes.append(new_node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Return a list of (alt_text, url) tuples for markdown images."""

    any_except_brackets = r"[^\[\]]*"
    any_except_parantheses = r"[^\(\)]*"
    matches = re.findall(rf"!\[({any_except_brackets})\]\(({any_except_parantheses})\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Return a list of (anchor_text, url) tuples for markdown links."""

    any_except_brackets = r"[^\[\]]*"
    any_except_parantheses = r"[^\(\)]*"
    matches = re.findall(rf"(?<!!)\[({any_except_brackets})\]\(({any_except_parantheses})\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        markdown_images = extract_markdown_images(old_node.text)
        remainder_text = old_node.text

        for alt_text, url in markdown_images:
            text_before, remainder_text = remainder_text.split(f"![{alt_text}]({url})", maxsplit=1)
            if text_before:
                new_nodes.append(TextNode(text=text_before, text_type=TextType.TEXT))

            node = TextNode(text=alt_text, text_type=TextType.IMAGE, url=url)
            new_nodes.append(node)

        if remainder_text:
            new_nodes.append(TextNode(text=remainder_text, text_type=TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        markdown_links = extract_markdown_links(old_node.text)
        remainder_text = old_node.text

        for anchor_text, url in markdown_links:
            text_before, remainder_text = remainder_text.split(f"[{anchor_text}]({url})", maxsplit=1)
            if text_before:
                new_nodes.append(TextNode(text=text_before, text_type=TextType.TEXT))

            node = TextNode(text=anchor_text, text_type=TextType.LINK, url=url)
            new_nodes.append(node)

        if remainder_text:
            new_nodes.append(TextNode(text=remainder_text, text_type=TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes
