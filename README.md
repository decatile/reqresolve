# bartender

A lightweight CLI tool for pinning package versions based on historical requirements in Git repositories.

## What It Does

bartender analyzes the history of your requirements.txt or pyproject.toml file and generates a new version with each
package pinned to the exact version that was available at the time of
its last change. This is especially useful for:

- Reproducing old builds from historical code
- Ensuring reproducibility when dependencies were locked by commit history
- Debugging issues caused by outdated or incompatible dependency versions

## How It Works

1. Uses git blame to find the most recent change to your requirements file
2. For each package listed in the file:
    - Queries PyPI for all available releases
    - Finds the latest version that was uploaded before the last change to the file
3. Outputs a new requirements file with versions pinned like: requests<=2.25.1

## CLI Usage

### Query Mode - Direct Package Information

Query package information directly from the command line without reading files:

```bash
bartender query <packages> -t <time>
```

Arguments:

- packages - One or more package names to query (required)
- -t, --time - Time before which to query package versions (required)

Examples:

```bash
# Using Unix timestamp
bartender query numpy pandas -t 1640995200

# Using ISO format date
bartender query requests flask -t "2023-01-01T00:00:00"

# Querying multiple packages
bartender query django numpy tensorflow -t "2022-06-15"
```

### File Mode - Work with Dependency Files

Analyzes and updates dependency files in a repository:

```bash
bartender file [options]
```

Arguments:

- -r, --root - Root directory of the repository (default: .)
- -f, --file - Relative path to the requirements file (default: requirements.txt)
- -d, --dry-run - Test mode, outputs results to console without writing to file

Examples:

```bash
# Analyze the default requirements.txt file in the current directory
bartender file

# Analyze a specific file in a given directory
bartender file --root /path/to/project --file requirements/dev.txt

# Test run to preview results
bartender file --dry-run

# Analyze an alternative dependency file
bartender file --file pyproject.toml
```

File Format Support

The tool supports standard package names and extras:

```
requests>=2.0.0
django[dev]==4.1.7
pyyaml<6.0
```

It correctly parses:

- package
- package==version
- package>=version
- package[extra] (e.g., numpy[testing])
- package[extra]==version

> ⚠️ Only the base name is used to query PyPI. Extras are preserved in output.

## Safety & Features

- Backups: By default, it backs up your original file with .bak extension if overwriting
- No external state: Works purely from Git history and PyPI metadata
- Async I/O: Fast parallel queries to PyPI using httpx
- Rich CLI output: Clear progress messages and status updates

## Limitations

- Only works with packages hosted on PyPI (https://pypi.org)
- Does not handle private repositories or custom indexes
- Version resolution assumes that the last change to requirements.txt reflects when a dependency was locked — may be
  inaccurate if changes were made without updating versions

## Installation

### Install from source:

```bash
git clone https://github.com/decatile/bartender.git
cd bartender
pip install -e .
```

## License

MIT — see [LICENSE](LICENSE) for details.

## Feedback & Contributions

Found a bug? Want new features (like support for pipenv, poetry, or custom indexes)?
Open an issue or submit a pull request!

> ✨ Contributions welcome
