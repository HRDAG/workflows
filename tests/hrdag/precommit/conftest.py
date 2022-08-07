import os
import pathlib

import click
import click.testing
import pytest


def build_dir(path, structure):
    path.mkdir(parents=True)
    for name, node in structure.items():
        child = path / name
        if isinstance(node, dict):
            build_dir(child, node)
        elif isinstance(node, str):
            child.write_text(node)
        elif isinstance(node, bytes):
            child.write_bytes(node)
        else:
            raise NotImplementedError


@pytest.fixture
def project_structure():
    return {".git": {}}


@pytest.fixture
def project_path(tmp_path, project_structure):
    path = pathlib.Path(tmp_path) / "project"
    build_dir(path, project_structure)
    return path


@pytest.fixture
def runner():
    return click.testing.CliRunner(mix_stderr=False)


@pytest.fixture
def relative_working_dir():
    return pathlib.Path(".")


@pytest.fixture
def working_dir(project_path, relative_working_dir):
    return project_path / relative_working_dir


@pytest.fixture
def set_cwd(project_path, working_dir):
    restore_to = pathlib.Path.cwd()
    try:
        os.chdir(working_dir)
        yield
    finally:
        os.chdir(restore_to)
