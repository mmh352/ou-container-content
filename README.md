# OU Container Content

![Validation Status](https://github.com/mmh352/ou-container-content/workflows/Validation/badge.svg) ![Tests](https://github.com/mmh352/ou-container-content/workflows/Tests/badge.svg)

# Install and Run

To run the OU Container Content you need to install the following two requirements:

* [Python 3.8 (or higher)](https://www.python.org/downloads/)
* [Pipx](https://pipxproject.github.io/pipx/)

Then, to install the OU Container Content run

```
pipx install git+https://github.com/mmh352/ou-container-content.git
```

You can then run the OU Container Content using the following command:

```
ou-container-content
```

## Development

To work on the OU Container Content you need to install an additional dependency:

* [Poetry](https://python-poetry.org/)

Then use

```
poetry install
```

to install all Python dependencies in a project-specific virtualenv. Then start a shell that runs commands
within that virtualenv:

```
poetry shell
```

You can now run

```
ou-container-content
```

to run your development version of the code.

### Validation

To automatically check that any committed code follows the Python guidelines, install a git pre-commit hook using
the following command:

```
pre-commit install
```

Validation checks are automatically run and must be passed before code can be merged into the default branch.
