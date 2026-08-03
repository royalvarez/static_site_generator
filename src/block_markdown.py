

def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")

    new_blocks = []
    for block in blocks:
        if block == '':
            continue

        new_blocks.append(block.strip())
    return new_blocks