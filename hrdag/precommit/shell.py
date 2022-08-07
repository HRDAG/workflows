import pathlib
import sys


def find_in(path: pathlib.Path, name: str):
    for child in path.iterdir():
        if child.name == name:
            return child
    else:
        return None


def repository_root():
    current_path = pathlib.Path.cwd()
    while current_path.parents:
        git_dir = find_in(current_path, ".git")
        if git_dir and git_dir.is_dir():
            return current_path
        else:
            current_path = current_path.parent
    sys.exit("Must be used within git repository")
