
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


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