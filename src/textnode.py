
from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode('b', textnode.text)
        case TextType.ITALIC:
            return LeafNode('i', textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            if textnode.url is None:
                raise ValueError("invalid url")
            return LeafNode('a', textnode.text, {"href": f"{textnode.url}"})
        case TextType.IMAGE:
            if textnode.url is None:
                raise ValueError("invalid url")
            return LeafNode("img", "", {"src": f"{textnode.url}", "alt": f"{textnode.text}"})
        case _:
            raise ValueError(f"invalid text type: {textnode.text_type}")
