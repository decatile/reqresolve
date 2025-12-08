# 📦 Pin Package Versions Based on Historical Requirements

A lightweight CLI tool that analyzes the history of a `requirements.txt` or `pyproject.toml` file in a Git repository and generates a new version of it, pinning each package to the **exact version that was available at the time of its last change**.

This is especially useful for:
- Reproducing old builds from historical code.
- Ensuring reproducibility when dependencies were locked by commit history.
- Debugging issues caused by outdated or incompatible dependency versions.

---

## 🔧 How It Works

1. **Finds the most recent change** to your `requirements.txt` file using Git blame (`git blame`).
2. For each package listed in the file:
    - Queries PyPI for all available releases.
    - Finds the latest version that was uploaded *before* the last change to the file.
3. Outputs a new `requirements.txt` with versions pinned like:
```txt
requests<=2.25.1
numpy<=1.20.0
   ```

> ✅ No need to manually track down old package versions — this tool does it automatically.

---

# CLI Usage

The program provides two main modes of operation:

## 1. `query` Mode - Query Packages Without Reading Files

Allows you to query package information directly from the command line.

**Syntax:**
```bash
reqresolve query <packages> -t <time>
```

**Arguments:**
- `packages` - One or more package names to query (required)
- `-t`, `--time` - Time before which to query package versions (required)

**Examples:**
```bash
# Using Unix timestamp
reqresolve query numpy pandas -t 1640995200

# Using ISO format date
reqresolve query requests flask -t "2023-01-01T00:00:00"

# Querying multiple packages
reqresolve query django numpy tensorflow -t "2022-06-15"
```

**Time formats for `--time`:**
- Unix timestamp (integer): `1640995200`
- ISO 8601 format: `"2023-01-01T00:00:00"` or `"2023-01-01"`

## 2. `file` Mode - Work with Dependency Files

Analyzes and updates dependency files in a repository.

**Syntax:**
```bash
reqresolve file [options]
```

**Arguments:**
- `-r`, `--root` - Root directory of the repository (default: `.`)
- `-f`, `--file` - Relative path to the requirements file (default: `requirements.txt`)
- `-d`, `--dry-run` - Test mode, outputs results to console without writing to file

**Examples:**
```bash
# Analyze the default requirements.txt file in the current directory
reqresolve file
```
This will:
- Analyze changes in `requirements.txt`
- Backup to `requirements.txt.bak`
- Generate a new file `requirements.txt` with pinned versions

**Also...**

```bash
# Analyze a specific file in a given directory
reqresolve file --root /path/to/project --file requirements/dev.txt

# Test run to preview results
reqresolve file --dry-run

# Analyze an alternative dependency file
reqresolve file --file pyproject.toml
```

## General Help

To get help on available commands:
```bash
reqresolve --help
```

To get help on a specific command:
```bash
reqresolve query --help
reqresolve file --help
```

---

## 📂 File Format Support

The tool supports standard package names and extras:

```txt
requests>=2.0.0
django[dev]==4.1.7
pyyaml<6.0
```

It correctly parses:
- `package`
- `package==version`
- `package>=version`
- `package[extra]` (e.g., `numpy[testing]`)
- `package[extra]==version`

> ⚠️ Only the base name is used to query PyPI. Extras are preserved in output.

---

## 🛡️ Safety & Features

- **Backups**: By default, it backs up your original file with `.bak` extension if overwriting.
- **No external state**: Works purely from Git history and PyPI metadata.
- **Async I/O**: Fast parallel queries to PyPI using `httpx`.
- **Rich CLI output**: Clear progress messages and status updates.

---

## 📌 Limitations

- Only works with packages hosted on [PyPI](https://pypi.org).
- Does not handle private repositories or custom indexes.
- Version resolution assumes that the *last change* to `requirements.txt` reflects when a dependency was locked — may be inaccurate if changes were made without updating versions.

---

## 📝 License

MIT — see [LICENSE](LICENSE) for details.

---

## 💬 Feedback & Contributions

Found a bug? Want new features (like support for `pipenv`, `poetry`, or custom indexes)?  
Open an issue or submit a pull request!

> ✨ **Contributions welcome!**
