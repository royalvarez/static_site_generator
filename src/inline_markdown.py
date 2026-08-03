
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        extract_image = extract_markdown_images(text)

        if len(extract_image) == 0:
            new_nodes.append(node)
            continue
        
        not_process_text = text
        for i in range(len(extract_image)):
            alt, url = extract_image[i]
            sections = not_process_text.split(f"![{alt}]({url})", maxsplit=1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            left_section = sections[0]
            right_section = sections[1]

            # add node type  based on position
            if left_section != '':
                # image is in between text
                new_nodes.append(TextNode(left_section, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            not_process_text = right_section

        if len(not_process_text) != 0:
            new_nodes.append(TextNode(not_process_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        extract_link = extract_markdown_links(text)

        if len(extract_link) == 0:
            new_nodes.append(node)
            continue
        
        not_process_text = text
        for i in range(len(extract_link)):
            alt, url = extract_link[i]
            sections = not_process_text.split(f"[{alt}]({url})", maxsplit=1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            left_section = sections[0]
            right_section = sections[1]

            # add node type  based on position
            if left_section != '':
                # link is in between text
                new_nodes.append(TextNode(left_section, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, url))
            not_process_text = right_section

        if len(not_process_text) != 0:
            new_nodes.append(TextNode(not_process_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    image_pattern = r"!\[([^.\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_pattern = r"(?<!!)\[([^.\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches