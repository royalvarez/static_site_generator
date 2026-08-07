
from pathlib import Path

import shutil


def copy_static_to_public(from_path: Path, destination_path: Path):
    if not destination_path.exists():
        Path.mkdir(destination_path)
    remove_public_contents()
    copy_static_to_public_r(from_path, destination_path)


def copy_static_to_public_r(from_path: Path, destination_path: Path):
    for child in from_path.iterdir():
        if child.is_dir():
            sub_directory = child.name
            new_destination_path = Path.joinpath(destination_path, f"{sub_directory}/")
            Path.mkdir(new_destination_path)
            copy_static_to_public_r(child, new_destination_path)
        else:
            shutil.copy(child, destination_path)


def remove_public_contents():
    root = Path.cwd()
    public_folder = Path.joinpath(root, "public/")
    remove_public_contents_r(public_folder)


def remove_public_contents_r(directory: Path):
    for child in directory.iterdir():
        if child.is_dir():
            remove_public_contents_r(child)
            Path.rmdir(child)
        else:
            Path.unlink(child)