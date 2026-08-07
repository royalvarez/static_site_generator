
from enum import Enum

from htmlnode import HTMLNode, ParentNode

from inline_markdown import text_to_textnodes

from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = blocks_to_html_nodes(blocks)

    return ParentNode("div", children, None)


def                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     blocks_to_html_nodes(blocks: list[str]) -> list[ParentNode]:
    parent_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            parent_nodes.append(paragraph_to_html_node(block))

        elif block_type == BlockType.HEADING:
                parent_nodes.append(heading_to_html_node(block))

        elif block_type == BlockType.CODE:
            parent_nodes.append(code_to_html_node(block))

        elif block_type == BlockType.QUOTE:
            parent_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.ULIST:
            parent_nodes.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.OLIST:
            parent_nodes.append(ordered_list_to_html_node(block))
        else:
            raise ValueError("invalid block type")
    return parent_nodes


def text_to_children(block: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(block)
    children = []

    for node in text_nodes:
            html_node = text_node_to_html_node(node)
            children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children, None)


def heading_to_html_node(block: str) -> ParentNode:
    heading_level = 0
    for character in block:
        if character == "#":
            heading_level += 1
        else:
            break
    if heading_level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {heading_level}")

    text = block[heading_level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{heading_level}", children, None)

def code_to_html_node(block: str) -> ParentNode:
    raw_text = block[4:-3]
    raw_text = raw_text.replace('&', "&amp;")
    raw_text = raw_text.replace('<', "&lt;")
    text_node = TextNode(raw_text, TextType.TEXT, None)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child], None)
    return ParentNode("pre", [code], None)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_line = line.lstrip(">").lstrip()
        new_lines.append(new_line)

    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children, None)


def unordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    html_items = []

    for line in lines:
        text = line[2:]
        item_children = text_to_children(text)
        html_node = ParentNode("li", item_children, None)
        html_items.append(html_node)
    return ParentNode("ul", html_items, None)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []

    i = 1
    for item in items:
        text = item[len(f"{i}. "):]
        item_children = text_to_children(text)
        html_node = ParentNode("li", item_children, None)
        html_items.append(html_node)
    return ParentNode("ol", html_items, None)


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")

    new_blocks = []
    for block in blocks:
        if block == '':
            continue

        new_blocks.append(block.strip())
    return new_blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        num = 1
        for line in block.split('\n'):
            if not line.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            num += 1
            
        return BlockType.OLIST

    return BlockType.PARAGRAPH