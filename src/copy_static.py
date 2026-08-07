
from pathlib import Path

import shutil


def copy_static_to_public():
    root = Path.cwd()
    sorce_folder = Path.joinpath(root, "static/")
    target_folder = Path.joinpath(root, "public/")
    if not target_folder.exists():
        Path.mkdir(target_folder)
    remove_public_contents()
    copy_static_to_public_r(sorce_folder, target_folder)


def copy_static_to_public_r(directory: Path, target_directory: Path):
    for child in directory.iterdir():
        if child.is_dir():
            sub_directory = child.name
            new_target_directory = Path.joinpath(target_directory, f"{sub_directory}/")
            Path.mkdir(new_target_directory)
            copy_static_to_public_r(child, new_target_directory)
        else:
            shutil.copy(child, target_directory)


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