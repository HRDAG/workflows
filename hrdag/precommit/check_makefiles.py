import pathlib
import sys

import click

from hrdag.precommit import shell

DEFAULT_EXEMPT_LIST = [
    "share",
]


def check_makefiles_in(path, exemptions):
    problem_paths = []

    if path not in exemptions:
        src = shell.find_in(path, "src")
        if src and src.is_dir():
            # Check conformance
            makefile = shell.find_in(path, "Makefile")
            if not (makefile and makefile.is_file()):
                problem_paths.append(path)

    for child in path.iterdir():
        if child.is_dir():
            problem_paths.extend(check_makefiles_in(child, exemptions))

    return problem_paths


@click.command("check-makefiles")
def main():
    cwd = pathlib.Path.cwd()
    exempt_set = {cwd / e for e in DEFAULT_EXEMPT_LIST}
    problem_paths = check_makefiles_in(shell.repository_root(), exempt_set)
    if problem_paths:
        click.secho("Missing Makefile:", err=True, fg="red")
        for path in sorted(problem_paths):
            click.secho(f"  {path.relative_to(cwd)}", err=True, fg="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
