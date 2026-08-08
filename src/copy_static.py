
from pathlib import Path

import shutil


def copy_static(from_path: Path, destination_path: Path):
    if not destination_path.exists():
        Path.mkdir(destination_path)
    copy_static_r(from_path, destination_path)


def copy_static_r(from_path: Path, destination_path: Path):
    for child_path in from_path.iterdir():
        if child_path.is_dir():
            sub_directory_name = child_path.name
            new_destination_path = Path.joinpath(destination_path, f"{sub_directory_name}/")
            Path.mkdir(new_destination_path)
            copy_static_r(child_path, new_destination_path)
        else:
            shutil.copy(child_path, destination_path)