
from textnode import TextNode, TextType

import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        split_nodes = []
        sections = text.split(delimiter)
        if (len(sections) % 2) == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            section = sections[i]
            if section == '':
                continue

            # determine if the current section contained the delimiter
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    image_pattern = r"!\[([^.\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_pattern = r"(?<!!)\[([^.\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches