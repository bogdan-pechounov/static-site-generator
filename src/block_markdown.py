from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes


def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=text_to_children(block.replace("\n", " ")))
        case BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level >= len(block) or block[level] != " ":
                raise ValueError("invalid heading format")
            text = block[level + 1 :]
            children = text_to_children(text)
            return ParentNode(f"h{level}", children)
        case BlockType.CODE:
            code_content = block[4:-3]
            return ParentNode("pre", children=[LeafNode(tag="code", value=code_content)])
        case BlockType.QUOTE:
            lines = block.split("\n")
            quote = " ".join([line.lstrip(">").strip() for line in lines])
            return ParentNode(tag="blockquote", children=text_to_children(quote))
        case BlockType.ORDERED_LIST:
            items = block.split("\n")
            html_items: list[HTMLNode] = []
            for item in items:
                _, text = item.split(". ", 1)
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ol", html_items)
        case BlockType.UNORDERED_LIST:
            items = block.split("\n")
            html_items: list[HTMLNode] = []
            for item in items:
                _, text = item.split("- ", 1)
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ul", html_items)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)

    return ParentNode("div", children)
