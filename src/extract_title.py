
def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    title = ""
    for line in lines:
        if line.startswith("# "):
            title += line.lstrip("#").strip()
            return title
    raise ValueError("Invalid markdown, missing title")