
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


def generate_pages_r(from_path: Path, template_path: Path, destination_path: Path):
    if not template_path.exists():
        raise ValueError(f"Invalid path: {template_path} could not be found")

    for child_path in from_path.iterdir():
        if child_path.is_dir():
            new_from_path = child_path
            new_destination_path = destination_path.joinpath(child_path.name)
            generate_pages_r(new_from_path, template_path, new_destination_path)

        else:
            for file_path in from_path.iterdir():
                if file_path.is_dir():
                    continue
                from_file_path = Path.joinpath(from_path, file_path.name)

                if not str(from_file_path).endswith(".md"):
                    raise ValueError(f"Invalid extension type: {from_path} must be markdown")

                destination_file_path = Path.joinpath(destination_path, file_path.name)
                convert_extension = str(destination_file_path).replace(".md", ".html")
                destination_file_path = Path(convert_extension)
            
                print(f"Generating page from {from_file_path} to {destination_file_path} using {template_path}")

                if not from_file_path.exists():
                    raise ValueError(f"Invalid path: {from_file_path} could not be found")

                markdown = from_file_path.read_text()

                template_content = template_path.read_text()

                html = markdown_to_html_node(markdown).to_html()
                html_title = extract_title(markdown)
            
                template_content = template_content.replace("{{ Title }}", html_title)
                template_content  = template_content.replace("{{ Content }}", html)

                if not destination_path.exists():
                    destination_path.mkdir(parents=True)

                if not destination_file_path.exists():
                    Path.touch(destination_file_path, exist_ok=True)
                destination_file_path.write_text(template_content)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    title = ""
    for line in lines:
        if line.startswith("# "):
            title += line.lstrip("#").strip()
            return title
    raise ValueError("Invalid markdown, missing title")