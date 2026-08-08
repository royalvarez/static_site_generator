
from copy_static import copy_static

from pathlib import Path

import shutil

from generate_page import generate_pages_r

import sys


base_path = "/" if len(sys.argv) <2 else sys.argv[1]

root = Path.cwd()
dir_static = Path.joinpath(root, "static/")
dir_docs = Path.joinpath(root, "docs/")

dir_content = Path.joinpath(root, "content")
dir_template = Path.joinpath(root, "template.html")
dir_destination = Path.joinpath(root, "docs/")

def main():
    if dir_docs.exists():
        shutil.rmtree(dir_docs)

    copy_static(dir_static, dir_docs)
    generate_pages_r(dir_content, dir_template, dir_destination, base_path)


if __name__ == "__main__":
    main()