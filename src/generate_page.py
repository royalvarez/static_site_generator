
from pathlib import Path

from block_markdown import markdown_to_html_node


def generate_page(from_path: Path, template_path: Path, destination_path: Path):
    print(f"Generating page from {from_path} to {destination_path} using {template_path}")

    if not from_path.exists():
        raise ValueError(f"Invalid path: {from_path} could not be found")

    markdown = from_path.read_text()

    if not template_path.exists():
        raise ValueError(f"Invalid path: {template_path} could not be found")

    template_content = template_path.read_text()

    html = markdown_to_html_node(markdown).to_html()
    html_title = extract_title(markdown)

    template_content = template_content.replace("{{ Title }}", html_title)
    template_content  = template_content.replace("{{ Content }}", html)

    if not destination_path.exists():
        Path.touch(destination_path, exist_ok=True)
    destination_path.write_text(template_content)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    title = ""
    for line in lines:
        if line.startswith("# "):
            title += line.lstrip("#").strip()
            return title
    raise ValueError("Invalid markdown, missing title")