"""Script to prepare the version information for a release."""
import re


VERSION = '1.0.0-b1'


def readlines(filename: str) -> list[str]:
    """Read a file as a list of lines."""
    with open(filename) as in_f:
        return in_f.readlines()


def writelines(filename: str, lines: list[str]):
    """Write a list of lines to a file."""
    with open(filename, 'w') as out_f:
        out_f.write(''.join(lines))


def update_version(filename: str, pattern: str, version: str):
    """Update the version in a file."""
    def replace_version(line: str) -> str:
        if re.match(pattern, line):
            return re.sub(r'[0-9]+\.[0-9]+\.[0-9]+(-b[0-9]+)?', version, line)
        else:
            return line

    writelines(filename, map(replace_version, readlines(filename)))


update_version('app/package.json', r'^  "version": "[0-9]+\.[0-9]+\.[0-9]+(-b[0-9]+)?",$', VERSION)
update_version('pyproject.toml', r'^version = "[0-9]+\.[0-9]+\.[0-9]+(-b[0-9]+)?"$',  VERSION)
